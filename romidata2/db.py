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
        if factory == None:
            self.__factory = DefaultFactory()
        else:
            self.__factory = factory
        self.__all = None
        
    def __del__(self):
        if self.__basefs:
            print(self.__basefs)
            self.__basefs.close()
            self.__basefs = None
        
    def get_by_id(self, id: str) -> IFarm:
        r = None
        for i in self.all:
            if i.id == id:
                r = i
                break
        return r
        
    def get_by_name(self, name: str) -> Any:
        r = None
        for i in self.all:
            if i.short_name == name:
                r = i
                break
        return r
        
    def get(self, id_or_short_name: str) -> IFarm:
        return (self.get_by_id(id_or_short_name)
                or self.get_by_name(id_or_short_name))
    
    def __append(self, obj: Any) -> None:
        if self.__all == None:
            self.__all = [ obj ]
        else:
            self.__all.append(obj)
        
    def __check_append(self, obj: Any) -> None:
        if not self.get(obj.id):
            self.__append(obj)
            
    def store(self, obj: Any) -> None:
        self.__makedirs(self.__typename, obj.id)
        relpath = fs.path.join(self.__typename, obj.id, self.__indexfile)
        with self.__basefs.open(relpath, 'w') as f:
            json.dump(obj, f, indent=4, cls=JsonExporter)
        self.__check_append(obj)
            
    def __load_one(self, obj_id: str) -> Any:
        farm = None
        relpath = fs.path.join(self.__typename, obj_id, self.__indexfile)
        with self.__basefs.open(relpath) as json_file:
            properties = json.load(json_file)
            farm = self.__factory.create(self.__classname, properties)
        return farm
    
    def __load_all(self):
        ids = self.__basefs.listdir(self.__typename)
        array = []
        for obj_id in ids:
            obj = self.__load_one(obj_id)
            array.append(obj)
        return array

    @property
    def all(self) -> List[Any]:
        if self.__all == None:
            self.__all = self.__load_all()
        return self.__all


    def new_file(self, parent: Any, source_name: str, source_id: str,
                 short_name: str, relpath: str, mimetype: str) -> IFile:
        f = self.__factory.create("File", {
            "id": new_id(),
            "source_name": source_name,
            "source_id": source_id,
            "short_name": short_name,
            "path": relpath,
            "mimetype": mimetype })
        f.parent = parent
        return f
    
    def get_file(self, top_id, sub_id, file_id) -> IFile:
        top = self.get(top_id)
        if not top:
            raise ValueError("Can't find %s entry with ID %s" % (self.__typename, top_id))
        sub = top.get(sub_id)
        if not sub:
            raise ValueError("Can't find %s entry with ID %s" % (self.__subtypename, sub_id))
        zfile = sub.get_file(file_id)
        if not zfile:
            raise ValueError("Can't find file with ID %s" % file_id)
        return zfile
        
    def __makedirs(self, *dirs) -> None:
        relpath = fs.path.join(*dirs)
        self.__basefs.makedirs(relpath, recreate=True)
            
    def __open_file(self, top_id: str, sub_id: str, relpath: str, mode: str):
        path = fs.path.dirname(relpath) 
        self.__makedirs(self.__typename, top_id, self.__subtypename, sub_id, path)
        relpath = fs.path.join(self.__typename, top_id, self.__subtypename, sub_id, relpath)
        return self.__basefs.open(relpath, mode=mode)

    def __open_ifile(self, zfile: IFile, mode: str):
        sub = zfile.parent
        top = sub.parent
        return self.__open_file(top.id, sub.id, zfile.path, mode)
        
    def file_store_text(self, ifile: IFile, text: str) -> None:
        f = self.__open_ifile(ifile, "w")
        f.write(text)
        f.close()
        
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

    
