import sys
from os.path import abspath
import argparse
from datetime import datetime, timedelta
import json
import statistics

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
    num_plants = 0
    num_dates = 0
    
    with open(args.files[0], 'r+') as f:
        lines = f.read().splitlines()

        num_plants = len(lines)
        date_values = []
        dates = []

        for plant_index in range(num_plants):
            line = lines[plant_index]
            values = line.split(' ')
            
            if num_dates == 0:
                num_dates = len(values)
                dates = [0] * num_dates
                date_values = [None] * num_dates
                date = start_date
                for date_index in range(num_dates):
                    dates[date_index] = date.isoformat()
                    date_values[date_index] = [0] * num_plants
                    date += timedelta(days=1)
                
            if num_dates != len(values):
                raise ValueError("Not all curves have the same length!")
            
            for date_index in range(num_dates):
                date_values[date_index][plant_index] = float(values[date_index])
                

        avg = [0] * num_dates
        stdev = [0] * num_dates
        for date_index in range(len(date_values)):
            a = date_values[date_index]
            avg[date_index] = statistics.mean(a)
            stdev[date_index] = statistics.stdev(a)

        #print("Values")
        #print(date_values)
        #print("Avg")
        #print(avg)
        #print("Stdev")
        #print(stdev)
            
        for plant_index in range(num_plants):
            plant = plants[plant_index]
            plant_observation = db.lookup(plant['observation_unit'])
            growth_analysis = proto.get_analysis("plant_growth")
            growth_analysis.observation_unit = plant_observation
            growth_analysis.state = IAnalysis.STATE_FINISHED
            
            curve = []
            for date_index in range(num_dates):
                point = {'date': dates[date_index],
                         'value': date_values[date_index][plant_index],
                         'mean': avg[date_index],
                         'stdev': stdev[date_index] }
                curve.append(point)
            result = { 'curve': curve }
            #print("Curve %d" % plant_index)
            #print(result)
            
            relpath = db.analysis_filepath(growth_analysis, "results", "json")
            output_file = db.new_file(farm.id,
                                      growth_analysis.short_name,
                                      growth_analysis.id,
                                      "results",
                                      relpath,
                                      "application/json")
            db.file_store_text(output_file, json.dumps(result, indent=4))
            db.store(growth_analysis)
            
