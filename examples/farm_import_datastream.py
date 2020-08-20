import sys
from os.path import abspath
import argparse
import json
from io import BytesIO
from datetime import datetime

import dateutil.parser
from tzlocal import get_localzone
from PIL import Image

sys.path.append(abspath('..'))
from romidata2.db import FarmDatabase
from romidata2.datamodel import IAnalysis
from romidata2.impl import DefaultFactory, new_id

    
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
    parser.add_argument("-z", "--zone", required=True,
                        help="The short name of the zone")
    parser.add_argument("--observable-name", required=True,
                        help="The human-readable name of the observable")
    parser.add_argument("--observable-id", required=True,
                        help="The URI of the observable")
    parser.add_argument("--unit-name", required=True,
                        help="The human-readable name of the unit")
    parser.add_argument("--unit-id", required=True,
                        help="The URI of the unit")
    parser.add_argument('files', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    db = FarmDatabase(args.db)
    factory = DefaultFactory()
    farm = db.get_farm(args.farm)
    if not farm:
        farms = db.select("Farm", "short_name", args.farm)
        if len(farms) >= 1:
            farm = farms[0]
    if not farm:
        raise ValueError("Can't find farm with id or short name %s" % args.farm)
    
    zone = farm.get_zone(args.zone)
    if not zone:
        raise ValueError("Can't find zone with id or short name %s" % args.zone)
    
    if len(args.files) != 1:
        raise ValueError("Expected one file to be passed on the command line")
        
    
    print("Import datastream")
    print("=================")
    print("Farm:              %s (%s)" % (farm.short_name, farm.id))
    print("Zone:              %s (%s)" % (zone.short_name, zone.id))

    datastream_id = new_id()
    relpath = db.datastream_filepath(farm, zone, datastream_id)
    datafile = db.new_file("datastreams", datastream_id,
                            "values", relpath, "application/json")

    datastream = factory.create("Datastream",
                                {
                                    "id": datastream_id,
                                    "file": datafile.id,
                                    "observable": { "id": args.observable_id,
                                                    "name": args.observable_name},
                                    "unit": { "id": args.unit_id, "name": args.unit_name}
                                })
    
    with open(args.files[0]) as f:
        data = json.load(f)
        db.file_store_json(datafile, data)
        db.store(datastream, False)

    zone.add_datastream(datastream, db)
