import sys
from os.path import abspath
import argparse
import json

sys.path.append(abspath('..'))
from romidata2.db import FarmDatabase
from romidata2.impl import DefaultFactory

    
def parse_list(s):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    return s.split(',')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create a new scan")
    parser.add_argument("-b", "--db", nargs='?', const="db",
                        help="The path to the database directory")
    parser.add_argument("-f", "--farm", required=True,
                        help="The short name of the farm")
    parser.add_argument("-u", "--observation-unit", required=True,
                        help="The short name or ID of the observation unit")
    parser.add_argument("--observable-name", required=True,
                        help="The human-readable name of the observable")
    parser.add_argument("--observable-uri", required=True,
                        help="The URI of the observable")
    parser.add_argument("--unit-name", required=True,
                        help="The human-readable name of the unit")
    parser.add_argument("--unit-uri", required=True,
                        help="The URI of the unit")
    parser.add_argument('files', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    db = FarmDatabase(args.db)
    factory = DefaultFactory(db)
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
        
    
    print("Import datastream")
    print("=================")
    print("Farm:              %s (%s)" % (farm.short_name, farm.id))
    print("Observation unit:  %s (%s)" % (observation_unit.short_name, observation_unit.id))

    datastream = factory.create("DataStream",
                                {
                                    "observation_unit": observation_unit.id,
                                    "file": "",
                                    "observable": {
                                        "uri": args.observable_uri,
                                        "name": args.observable_name
                                    },
                                    "unit": {
                                        "uri": args.unit_uri,
                                        "name": args.unit_name
                                    }
                                })
    datastream.observation_unit = observation_unit # FIXME
    
    relpath = db.datastream_filepath(datastream)
    datafile = db.new_file(farm.id, "datastreams", datastream.id, "values", relpath, "application/json")
    
    with open(args.files[0]) as f:
        data = json.load(f)
        db.file_store_json(datafile, data)

    datastream.file = datafile
    datastream.store()
