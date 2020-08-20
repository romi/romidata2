import sys
from os.path import abspath
import argparse
import json
from io import BytesIO
from datetime import datetime

from tzlocal import get_localzone
from PIL import Image
from romidata import FSDB

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.db import FarmDatabase
from romidata2.datamodel import IAnalysis


def create_date(year, month, day, hour=12, minutes=0, seconds=0) -> datetime:
    tz = get_localzone()
    return tz.localize(datetime(year, month, day, hour, minutes, seconds))

        
def analysis_store_results(db, farm, zone, analysis, results):
    relpath = db.analysis_filepath(farm, zone, analysis, "results", "json")
    output_file = db.new_file(analysis.short_name, analysis.id,
                              "results", relpath, "application/json")
    db.file_store_text(output_file, json.dumps(results, indent=4))
    #zone.add_file(output_file)
    
    
def parse_list(s):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    return s.split(',')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create a new scan")
    parser.add_argument("--fsdb", required=True,
                        help="The path of the FSDB directory")
    parser.add_argument("-b", "--db", nargs='?', const="db",
                        help="The path to the database directory")
    parser.add_argument("-P", "--proto", nargs='?', const="prototypes",
                        help="The path to the prototypes directory")
    parser.add_argument("-f", "--farm", required=True,
                        help="The short name of the farm")
    parser.add_argument("-z", "--zone", required=True,
                        help="The short name of the zone")
    parser.add_argument("-p", "--people", required=True,
                        help="A comma-separated list with the names of the operators")
    parser.add_argument("-c", "--camera", required=False,
                        help="The short name of the camera")
    parser.add_argument("-d", "--scanning-device", required=False,
                        help="The short name of the scanning device")
    parser.add_argument("-t", "--scan-path", required=True,
                        help="The short name of the scan path")
    parser.add_argument('scans', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    db = FarmDatabase(args.db)
    proto = Prototypes(args.proto)
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
    
    person_names = parse_list(args.people)
    for name in person_names:
        person = db.get_person(name)
        if not person:
            raise ValueError("Can't find person with id or short name %s" % name)

    
    print("Import scans")
    print("============")
    print("FSBD:              %s" % args.fsdb)
    print("Farm:              %s (%s)" % (farm.short_name, farm.id))
    print("Zone:              %s (%s)" % (zone.short_name, zone.id))
    print("Operators:         %s" % ", ".join(person_names))
    
    if args.camera:
        print("Camera:            %s" % args.camera)
    else:
        print("Camera:            default camera")
        
    if args.scanning_device:
        print("Scanning device:   %s" % args.scanning_device)
    else:
        print("Scanning device:   default scanner")

    print("Scan path:         %s" % args.scan_path)
    scan_path = proto.get_scan_path(args.scan_path)
    if not scan_path:
        raise ValueError("Can't find scan path %s" % s)

    newscan = zone.new_scan(db,
                            person_names = person_names,
                            camera_name = args.camera,
                            valid_cameras = farm.cameras,
                            scanning_device_name = args.scanning_device,
                            valid_scanning_devices = farm.scanning_devices,
                            scan_path = scan_path)
    
    fsdb = FSDB(args.fsdb)
    fsdb.connect()
    for scan_id in args.scans:
        print()
        print("Importing")
        print("=========")
        print("Scan:              %s" % scan_id)
        fsdb_scan = fsdb.get_scan(scan_id)
        if not fsdb_scan:
            print("Didn't find scan %s: skipping" % scan_id)
            continue
        d = fsdb_scan.get_metadata("date")
        year = int(d[0:4])
        month = int(d[4:6])
        day = int(d[6:8])
        newscan.date = create_date(year, month, day)
        
        images_fileset = fsdb_scan.get_fileset("images")
        if not images_fileset:
            images_fileset = fsdb_scan.get_fileset("raw_data")
        if not images_fileset:
            raise ValueError("Can't find images directory")
        images = images_fileset.get_files()
        for image in images:
            print("Importing %s" % image.filename)
            data = image.read_raw()
            relpath = db.scan_filepath(farm, zone, newscan, image.id, "jpg")
            image_file = db.new_file("scan", newscan.id,
                                     image.id, relpath, "image/jpeg")
            db.file_store_bytes(image_file, data)
            #zone.add_file(image_file)

        stitching = proto.get_analysis("stitching")
        stitching.scan_id = newscan.id
        stitching.state = IAnalysis.STATE_FINISHED
        stitching_task = stitching.tasks[0]
        results = {}
        
        maps_fileset = fsdb_scan.get_fileset("maps")
        images = maps_fileset.get_files()
        for image in images:
            data = image.read_raw()
            relpath = db.analysis_filepath(farm, zone, stitching, image.id, "png")
            output_file = db.new_file(stitching_task.short_name, stitching_task.id,
                                      image.id, relpath, "image/png")
            db.file_store_bytes(output_file, data)
            #zone.add_file(output_file)

            results[image.id] = output_file.id

            if image.id == "map":
                im = Image.open(BytesIO(data))
                w, h = im.size
                results["width"] = w
                results["height"] = h
                
            
        analysis_store_results(db, farm, zone, stitching, results)
        zone.add_analysis(stitching, db)

        plant_analysis = proto.get_analysis("plant_analysis")
        plant_analysis.scan_id = newscan.id
        plant_analysis.state = IAnalysis.STATE_FINISHED
        map_segmentation_task = plant_analysis.get_task("map_segmentation")
        plant_indexing_task = plant_analysis.get_task("plant_indexing")
        plant_growth_analysis_task = plant_analysis.get_task("plant_growth_analysis")

        tmp = {}
        
        locations = {}
        index = {}
        pla = {}
        plant_images = {}
        plant_masks = {}
        
        plant_analysis_fileset = fsdb_scan.get_fileset("individual_plants")
        files = plant_analysis_fileset.get_files()
        for fsdb_file in files:
            data = fsdb_file.read_raw()
            relpath = db.analysis_filepath(farm, zone, plant_analysis,
                                           fsdb_file.id, "png")
            output_file = db.new_file(map_segmentation_task.short_name,
                                      map_segmentation_task.id,
                                      fsdb_file.id, relpath, "image/png")
            db.file_store_bytes(output_file, data)
            #zone.add_file(output_file)

            fsdb_meta = fsdb_file.get_metadata()

            file_id = fsdb_file.id
            if "mask" in fsdb_file.id:
                file_id = fsdb_file.id.split("_")[0]

            if not file_id in tmp:
                tmp[file_id] = {}
            
            if "mask" in fsdb_file.filename:
                file_id = fsdb_file.id.split("_")[0]
                #plant_masks[file_id] = output_file.id
                tmp[file_id]["mask"] = output_file.id
            else:
                #plant_images[fsdb_file.id] = output_file.id
                #locations[fsdb_file.id] = fsdb_meta["loc"]
                #pla[fsdb_file.id] = fsdb_meta["PLA"]
                #index[fsdb_file.id] = fsdb_meta["id"]
                tmp[fsdb_file.id]["image"] = output_file.id
                tmp[fsdb_file.id]["location"] = fsdb_meta["loc"]
                tmp[fsdb_file.id]["id"] = fsdb_meta["id"]
                tmp[fsdb_file.id]["PLA"] = fsdb_meta["PLA"]
                
                im = Image.open(BytesIO(data))
                w, h = im.size
                tmp[fsdb_file.id]["width"] = w
                tmp[fsdb_file.id]["height"] = h
                
        results = {}
        plants = []
        for key in tmp.keys():
            plants.append(tmp[key])
        results["plants"] = plants
        analysis_store_results(db, farm, zone, plant_analysis,results)
        
        zone.add_analysis(plant_analysis, db)
        
    fsdb.disconnect()

    db.store(farm)
