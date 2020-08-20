#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""romidata2.db
===============

Provides the default implementation of the database. A generic
database (Database) is declined into two specialized databases,
FarmDatabase and InvestigationDatabase.

Examples
--------
>>> from romidata2.db import FarmDatabase
>>> db = FarmDatabase("demo/db")
>>> farm = db.get("farm000")

"""
from typing import List, Any
import json

from fs import open_fs
import fs

from romidata2.datamodel import *
from romidata2.impl import *
from romidata2.io import JsonImporter, JsonExporter

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class Database(IDatabase):
    def __init__(self,
                 basedir: str,
                 typename: str,
                 classname: str,
                 subtypename: str,
                 factory: IFactory = None):
        self.__basedir = basedir
        self.__typename = typename
        self.__subtypename = subtypename
        self.__classname = classname
        self.__indexfile = "index.json"
        self.__basefs = open_fs(self.__basedir, create=True)
        self.__objects = {}        
        self.__files = {}        
        if factory == None:
            self.__factory = DefaultFactory()
        else:
            self.__factory = factory
        self.__makedirs("objects")
        self.__makedirs("files")
        self.__makedirs("data")
        self.__load_files()
        self.__load_objects()

        
    def __del__(self):
        if self.__basefs:
            print(self.__basefs)
            self.__basefs.close()
            self.__basefs = None

    def __load_object(self, relpath: str) -> Any:
        obj = None
        if self.__basefs.exists(relpath):
            with self.__basefs.open(relpath) as json_file:
                data = json.load(json_file)
                obj = self.__factory.create(data["classname"],
                                            data["value"])
                self.__objects[data["id"]] = obj        
        return obj
    
    def __load_objects(self) -> None:
        for filename in self.__basefs.listdir('objects'):
            if filename.endswith(".json"):
                self.__load_object(fs.path.join("objects", filename))
        for obj in self.__objects.values():
            obj.restore(self)
                
    def __load_id(self, obj_id: str) -> None:
        relpath = fs.path.join("objects", "%s.json" % obj_id)
        return self.__load_object(relpath)

    def store_object(self, obj_id: str, classname: str, obj: Any) -> None:
        relpath = fs.path.join("objects", "%s.json" % obj_id)
        with self.__basefs.open(relpath, 'w') as f:
            data = {
                "id": obj_id,
                "classname": classname,
                "value": obj
            }
            json.dump(data, f, indent=4, cls=JsonExporter)
    
    def __insert(self, obj: BaseClass) -> None:
        self.__objects[obj.id] = obj

    def lookup(self, obj_id: str) -> BaseClass:
        r = self.__objects.get(obj_id)
        if r == None:
            r = self.__load_id(obj_id)            
        return r
            
    def select(self, classname: str, prop: str = None, value: str = None) -> List[BaseClass]:
        r = []
        for obj in self.__objects.values():
            if (obj.classname == classname
                and (prop == None 
                     or getattr(obj, prop) == value)):
                r.append(obj)
        return r
            
    def store(self, obj: Any, recursive=True) -> None:
        self.__insert(obj)
        obj.store(self, recursive)
        
    def __insert_file(self, ifile: IFile) -> None:
        self.__files[ifile.id] = ifile        

    def __load_file(self, relpath: str) -> None:
        with self.__basefs.open(relpath) as json_file:
            data = json.load(json_file)
            f = self.__factory.create("File", data)
            self.__insert_file(f)

    def __load_files(self) -> None:
        for filename in self.__basefs.listdir('files'):
            if filename.endswith(".json"):
                self.__load_file(fs.path.join("files", filename))

    def __store_file(self, ifile: IFile) -> None:
        relpath = fs.path.join("files", "%s.json" % ifile.id)
        with self.__basefs.open(relpath, 'w') as f:
            json.dump(ifile, f, indent=4, cls=JsonExporter)
        self.__insert_file(ifile)

    def new_file(self, source_name: str, source_id: str,
                 short_name: str, relpath: str, mimetype: str) -> IFile:
        f = self.__factory.create("File", {
            "id": new_id(),
            "source_name": source_name,
            "source_id": source_id,
            "short_name": short_name,
            "date_created": current_date().isoformat(),
            "source_name": source_name,
            "path": relpath,
            "mimetype": mimetype })
        self.__store_file(f)
        return f

    def get_file(self, file_id: str) -> IFile:
        return self.__files.get(file_id)
        
    def select_files(self,
                     source_name: str,
                     source_id: str,
                     short_name: str) -> List[IFile]:
        r = []
        for f in self.__files.values():
            if ((source_name == None or f.source_name == source_name)
                and (source_id == None or f.source_id == source_id)
                and (short_name == None or f.short_name == short_name)):
                r.append(f)
        return r
        
    def __makedirs(self, *dirs) -> None:
        relpath = fs.path.join(*dirs)
        self.__basefs.makedirs(relpath, recreate=True)
            
    def __open_file(self, relpath: str, mode: str):
        dirs = fs.path.dirname(relpath) 
        self.__makedirs(dirs)
        return self.__basefs.open(relpath, mode=mode)

    def __open_ifile(self, ifile: IFile, mode: str):
        return self.__open_file(fs.path.join("data", ifile.path), mode)
        
    def file_store_text(self, ifile: IFile, text: str) -> None:
        f = self.__open_ifile(ifile, "w")
        f.write(text)
        f.close()
        
    def file_store_json(self, ifile: IFile, value: Any) -> None:
        self.file_store_text(ifile, json.dumps(value, indent=4))
        
    def file_store_bytes(self, ifile: IFile, data: bytes) -> None:
        f = self.__open_ifile(ifile, "wb")
        f.write(data)
        f.close()
    
    def file_read_text(self, ifile: IFile) -> str:
        f = self.__open_ifile(ifile, "r")
        r = f.read()
        f.close()
        return r;

    def file_read_json(self, f: IFile) -> Any:
        s = self.file_read_text(f)
        return json.loads(s)
    
    def file_read_bytes(self, ifile: IFile) -> bytes:
        f = self.__open_ifile(ifile, "rb")
        r = f.read()
        f.close()
        return r;

    
class InvestigationDatabase(Database):
    def __init__(self, basedir: str, factory: IFactory = None):
        super().__init__(basedir, "investigations", "Investigation", "studies", factory)

        
class FarmDatabase(Database):
    def __init__(self, basedir: str, factory: IFactory = None):
        super().__init__(basedir, "farms", "Farm", "zones", factory)

    def get_person(self, person_id: str):
        r = self.lookup(person_id)
        if not r:
            people = self.select("Person", "short_name", person_id)
            if len(people) >= 1:
                r = people[0]
        return r

    def get_farm(self, farm_id: str):
        r = self.lookup(farm_id)
        if not r:
            farms = self.select("Farm", "short_name", farm_id)
            if len(farms) >= 1:
                r = farms[0]
        return r
    
    def get_zone(self, zone_id: str):
        r = self.lookup(zone_id)
        if not r:
            zones = self.select("Zone", "short_name", zone_id)
            if len(zones) >= 1:
                r = zones[0]
        return r

    def get_scan(self, scan_id: str):
        return self.lookup(scan_id)

    def get_analysis(self, analysis_id: str):
        return self.lookup(analysis_id)

    def get_datastream(self, stream_id: str):
        pass
    
    def scan_filepath(self, farm, zone, scan, file_short_name, ext):
        return "%s/%s/scans/%s/%s.%s" % (farm.short_name,
                                         zone.short_name,
                                         scan.date.strftime("%Y%m%d-%H%M%S"),
                                         file_short_name,
                                         ext)

    def analysis_filepath(self, farm, zone, analysis, file_short_name, ext):
        return "%s/%s/%s/%s/%s.%s" % (farm.short_name,
                                      zone.short_name,
                                      analysis.short_name,
                                      analysis.id,
                                      file_short_name,
                                      ext)

    def datastream_filepath(self, farm, zone, datastream_id):
        return "%s/%s/datastreams/%s.json" % (farm.short_name,
                                              zone.short_name,
                                              datastream_id)

