#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Any
from os import listdir
from os.path import isfile, join, splitext
import json

from fs import open_fs

from romidata2.datamodel import IFactory

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class JsonExporter(json.JSONEncoder):
    def default(self, o):
        return o.serialize()

    
class JsonImporter():
    def __init__(self, factory: IFactory):
        self.__factory = factory
        
    def load_dir(self, directory: str, classname: str) -> List[Any]:
        array = []
        fs = open_fs(directory)
        for path in fs.walk.files(filter=['*.json']):
            print("Loading %s from %s" % (classname, path)) # TODO: print name only
            with fs.open(path) as json_file:
                properties = json.load(json_file)
                obj = self.__factory.create(classname, properties)
                array.append(obj)
        return array
