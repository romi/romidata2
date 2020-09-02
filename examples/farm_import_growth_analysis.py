import sys
from os.path import abspath
import argparse
from datetime import datetime, timedelta
import json

import dateutil.parser

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.db import FarmDatabase
from romidata2.datamodel import IAnalysis
from romidata2.impl import DefaultFactory



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create a new scan")
    parser.add_argument("-b", "--db", nargs='?', const="db",
                        help="The path to the database directory")
    parser.add_argument("-P", "--proto", nargs='?', const="prototypes",
                        help="The path to the prototypes directory")
    parser.add_argument("-f", "--farm", required=True,
                        help="The short name of the farm")
    parser.add_argument("-u", "--observation-unit", required=True,
                        help="The short name or ID of the observation unit")
    parser.add_argument("--start-date", required=True,
                        help="The start date of the growth curve")
    parser.add_argument('files', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    db = FarmDatabase(args.db)
    factory = DefaultFactory(db)

    proto = Prototypes(args.proto)
    
    farm = db.get_farm(args.farm)
    if not farm:
        farms = db.select("Farm", "short_name", args.farm)
        if len(farms) >= 1:
            farm = farms[0]
    if not farm:
        raise ValueError("Can't find farm with id or short name %s" % args.farm)

    observation_unit = farm.get_observation_unit(args.observation_unit)
    if not observation_unit:
        raise ValueError("Can't find observation unit with id or name %s" % args.observation_unit)
    
    if len(args.files) != 1:
        raise ValueError("Expected one file to be passed on the command line")
    
    start_date = dateutil.parser.parse(args.start_date)
    
    print("Import growth curves")
    print("=================")
    print("Farm:              %s (%s)" % (farm.short_name, farm.id))
    print("Observation unit:  %s (%s)" % (observation_unit.short_name, observation_unit.id))
    print("Start Date:        %s" % start_date.isoformat())

    plant_analysis = None
    for analysis in observation_unit.analyses:
        if analysis.short_name == "plant_analysis":
            plant_analysis = analysis
            break

    if not plant_analysis:
        raise ValueError("Can't find the plant analysis in the observation unit")

    results = db.file_read_json(plant_analysis.results_file)
    plants = results.get("plants", [])
    
    with open(args.files[0], 'r+') as f:
        lines = f.read().splitlines()
        for i in range(len(lines)):
            line = lines[i]
            values = line.split(' ')
            plant = plants[i]
            plant_observation = db.lookup(plant['observation_unit'])
            date = start_date
            curve = []
            for value in values:
                point = {'date': date.isoformat(), 'value': float(value) }
                curve.append(point)
                date += timedelta(days=1)

            results = { 'curve': curve }
            growth_analysis = proto.get_analysis("plant_growth")
            growth_analysis.observation_unit = plant_observation
            growth_analysis.state = IAnalysis.STATE_FINISHED
            
            relpath = db.analysis_filepath(growth_analysis, "results", "json")
            output_file = db.new_file(farm.id,
                                      growth_analysis.short_name,
                                      growth_analysis.id,
                                      "results",
                                      relpath,
                                      "application/json")
            db.file_store_text(output_file, json.dumps(results, indent=4))
            db.store(growth_analysis)
            
