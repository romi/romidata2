#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""romidata2.impl
=================

Provides the default implementation of the data objects used in romidata2.

"""
from abc import ABC, abstractmethod
from typing import List, Any
import copy
import random
import string
import uuid
from datetime import datetime
import functools

from tzlocal import get_localzone
import dateutil.parser
import fs

from romidata2.datamodel import *

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"


def new_id() -> str:
    """Generates a new random ID."""
    return str(uuid.uuid4())


def current_date() -> datetime:
    """Generates a datetime object with the current date. The timezone will be set."""
    tz = get_localzone()
    return tz.localize(datetime.now())

        
def lookup_id_list(db: IDatabase, array: List[str]) -> List[Any]:
    r = []
    for the_id in array:
        obj = db.lookup(the_id)
        if obj:
            r.append(obj)
        else:
            raise ValueError("ID with value %s does not exist" % the_id)
    return r


def find(given_value: str, array: List[Any], attr: str):
    r = None
    for obj in array:
        obj_value = getattr(obj, attr)
        if obj_value == given_value:
            r = obj
            break
    return r


class BaseImpl():
    def __init__(self, factory, database, classname):
        self.__id = new_id()
        self.__classname = classname
        self.__modified = False
        self.__factory = factory
        self.__database = database

    def modifies(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.modified = True
            return func(self, *args, **kwargs)
        return wrapper

    @property
    def classname(self) -> str:
        return self.__classname
        
    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    @modifies
    def id(self, value: str):
        self.__id = value

    @property
    def modified(self) -> bool:
        return self.__modified

    @modified.setter
    def modified(self, value: bool) -> None:
        self.__modified = value

    @property
    def factory(self) -> IFactory:
        return self.__factory

    @property
    def database(self) -> Any:
        return self.__database

    def clone(self):
        c = copy.deepcopy(self)
        c.__id = new_id()
        c.__modified = True
        return c
    
    def store(self) -> None:
        self.database.store(self)

    def restore(self) -> None:
        pass

    @modifies
    def parse(self, properties: dict):
        if 'id' in properties:
            self.__id = properties['id']

    def serialize(self) -> dict:
        raise NotImplementedError()

    
class File(BaseImpl, IFile):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__owner_id = ""
        self.__source_name = ""
        self.__source_id = ""
        self.__short_name = ""
        self.__date_created = None
        self.__path = ""
        self.__mimetype = ""

    @property
    def owner(self) -> str:
        return self.__owner_id

    @property
    def source_name(self) -> List[str]:
        return self.__source_name

    @source_name.setter
    def source_name(self, value: List[str]):
        self.__source_name = value

    @property
    def source_id(self) -> List[str]:
        return self.__source_id

    @source_id.setter
    def source_id(self, value: List[str]):
        self.__source_id = value

    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def date_created(self) -> datetime:
        return self.__date_created

    @date_created.setter
    def date_created(self, value: datetime):
        self.__date_created = value
        
    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def mimetype(self) -> str:
        return self.__mimetype

    @mimetype.setter
    def mimetype(self, value: str):
        self.__mimetype = value

    ##
    
    def clone(self):
        raise NotImplementedError()
    
    def store(self) -> None:
        raise NotImplementedError()
        
    def parse(self, properties: dict):
        super().parse(properties)
        self.__owner_id = properties["owner"]
        self.source_name = properties["source_name"]
        self.source_id = properties["source_id"]
        self.short_name = properties["short_name"]
        self.date_created = dateutil.parser.parse(properties["date_created"])
        self.path = properties["path"]
        self.mimetype = properties["mimetype"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'owner': self.__owner_id,
                 'source_name': self.source_name,
                 'source_id': self.source_id,
                 'short_name': self.short_name,
                 'date_created': self.date_created.isoformat(),
                 'path': self.path,
                 'mimetype': self.mimetype }


class Person(BaseImpl, IPerson):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__name = ""
        self.__email = ""
        self.__affiliation = ""
        self.__role = ""
        
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self.__email = value

    @property
    def affiliation(self) -> str:
        return self.__affiliation

    @affiliation.setter
    def affiliation(self, value: str):
        self.__affiliation = value

    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, value: str):
        self.__role = value
        
    ##
        
    def store(self) -> None:
        self.database.store(self)
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.email = properties["email"]
        self.affiliation = properties["affiliation"]
        self.role = properties["role"]

    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'name': self.name,
                 'email': self.email,
                 'affiliation': self.affiliation,
                 'id': self.id,
                 'role': self.role }

    
class Camera(BaseImpl, ICamera):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
        self.__lens = ""
        self.__owner = None
        self.__owner_id = ""
        self.__software_module = None
        self.__parameters = None
        
    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        
    @property
    def lens(self) -> str:
        return self.__lens

    @lens.setter
    def lens(self, value: str):
        self.__lens = value

    @property
    def owner(self) -> Any:
        return self.__owner

    @owner.setter
    def owner(self, p: Any):
        self.__owner = p
        self.__owner_id = p.id
        
    @property
    def software_module(self) -> ISoftwareModule:
        return self.__software_module

    @software_module.setter
    def software_module(self, value: ISoftwareModule):
        self.__software_module = value

    @property
    def parameters(self) -> IParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, values: IParameters):
        self.__parameters = values
        
    ##
        
    def clone(self):
        c = super().clone()
        c.software_module = self.software_module.clone()
        c.parameters = self.parameters.clone()
        c.__owner_id = ""
        c.__owner = None
        return c;
    
    def restore(self) -> None:
        self.__owner = self.database.lookup(self.__owner_id)
        self.__owner.add_camera(self)
        
    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.lens = properties["lens"]
        self.__owner_id = properties["owner"]
        self.software_module = self.factory.create("SoftwareModule",
                                                   properties["software_module"])
        self.parameters = self.factory.create("Parameters",
                                              properties["parameters"])

    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'lens': self.lens,
                 'owner': self.__owner_id,
                 'software_module': self.software_module,
                 'parameters': self.parameters }


class ScanningDevice(BaseImpl, IScanningDevice):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
        self.__owner = None
        self.__owner_id = ""
        self.__software_module = None
        self.__parameters = None
        
    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def owner(self) -> Any:
        return self.__owner

    @owner.setter
    def owner(self, p: Any):
        self.__owner = p
        self.__owner_id = p.id
        
    @property
    def software_module(self) -> ISoftwareModule:
        return self.__software_module

    @software_module.setter
    def software_module(self, value: ISoftwareModule):
        self.__software_module = value
        
    @property
    def parameters(self) -> IParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: IParameters):
        self.__parameters = value

    ##
    
    def clone(self):
        c = super().clone()
        c.software_module = self.software_module.clone()
        c.parameters = self.parameters.clone()
        c.__owner_id = ""
        c.__owner = None
        return c; 
    
    def restore(self) -> None:
        self.__owner = self.database.lookup(self.__owner_id)
        self.__owner.add_scanning_device(self)
       
    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.__owner_id = properties["owner"]
        self.software_module = self.factory.create("SoftwareModule",
                                                   properties["software_module"])
        self.parameters = self.factory.create("Parameters",
                                              properties["parameters"])
        
    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'owner': self.__owner_id,
                 'software_module': self.software_module,
                 'parameters': self.parameters }

        
class Sample(BaseImpl, ISample):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__description = ""
        self.__development_stage = ""
        self.__anatomical_entity = ""
        
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        
    @property
    def development_stage(self) -> str:
        return self.__development_stage

    @development_stage.setter
    def development_stage(self, value: str):
        self.__development_stage = value

    @property
    def anatomical_entity(self) -> str:
        return self.__anatomical_entity

    @anatomical_entity.setter
    def anatomical_entity(self, value: str):
        self.__anatomical_entity = value

    ## 
    
    def store(self) -> None:
        raise NotImplementedError()

    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.description = properties["description"]
        self.development_stage = properties["development_stage"]
        self.anatomical_entity = properties["anatomical_entity"]
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'description': self.description,
                 'development_stage': self.development_stage,
                 'anatomical_entity': self.anatomical_entity }

    
class ObservationUnit(BaseImpl, IObservationUnit):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__type = ""
        self.__short_name = ""
        self.__context = None
        self.__context_id = ""
        self.__zone = None
        self.__zone_id = ""
        self.__spatial_distribution = ""
        self.__factor_values = {}
        self.__samples = []
        self.__parent = None
        self.__parent_id = ""
        self.__children = []
        self.__description_file = ""
        self.__scans = []
        self.__analyses = []
        self.__datastreams = []
        self.__notes = []
        
    @property
    def type(self) -> str:
        return self.__type

    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value

    @property
    def context(self) -> Any:
        return self.__context

    @context.setter
    def context(self, p: Any):
        self.__context = p
        self.__context_id = p.id
        
    @property
    def zone(self) -> Any:
        return self.__zone

    @zone.setter
    def zone(self, value: Any):
        self.__zone = value
        self.__zone_id = value.id
    
    @property
    def spatial_distribution(self) -> str:
        return self.__spatial_distribution

    @spatial_distribution.setter
    def spatial_distribution(self, value: str):
        self.__spatial_distribution = value

    @property
    def factor_values(self) -> dict:
        return self.__factor_values

    def set_factor_value(self, key: str, value: str):
        self.__factor_values[key] = value
        
    @property
    def description_file(self) -> str:
        return self.__description_file

    @description_file.setter
    def description_file(self, value: str):
        self.__description_file = value
    
    @property
    def samples(self) -> List[ISample]:
        return self.__samples

    def add_sample(self, sample: ISample):
        if find(sample.id, self.samples, "id") == None:
            self.__samples.append(sample)

    @property
    def parent(self) -> Any:
        return self.__parent

    @parent.setter
    def parent(self, value: Any) -> None:
        self.__parent = value
        self.__parent_id = value.id
        print("ObservationUnit.parent '%s'" % self.__parent_id)

    @property
    def children(self) -> List[Any]:
        return self.__children

    def add_child(self, child: Any) -> None:
        print("ObservationUnit.add_child")
        if find(child.id, self.children, "id") == None:
            self.children.append(child)
            child.parent = self
            
    @property
    def datastreams(self) -> List[IDataStream]:
        return self.__datastreams

    def add_datastream(self, datastream: IDataStream):
        if find(datastream.id, self.datastreams, "id") == None:
            self.datastreams.append(datastream)
            datastream.observation_unit = self
        
    @property
    def scans(self) -> List[Any]:
        return self.__scans
    
    def add_scan(self, scan: Any):
        if find(scan.id, self.scans, "id") == None:
            self.scans.append(scan)
            scan.observation_unit = self
            
    @property
    def analyses(self) -> List[IAnalysis]:
        return self.__analyses
        
    def add_analysis(self, analysis: IAnalysis):
        if find(analysis.id, self.analyses, "id") == None:
            self.analyses.append(analysis)
    
    @property
    def notes(self) -> List[INote]:
        return self.__notes
        
    def add_note(self, note: INote):
        if find(note.id, self.notes, "id") == None:
            note.observation_unit = self
            self.notes.append(note)

    ##

    def restore(self) -> None:
        self.__context = self.database.lookup(self.__context_id)
        self.__context.add_observation_unit(self)
        if self.__zone_id:
            self.__zone = self.database.lookup(self.__zone_id)
            self.__zone.add_observation_unit(self)
        print("ObservationUnit.restore: parent='%s'" % self.__parent_id)
        if self.__parent_id:
            self.__parent = self.database.lookup(self.__parent_id)
            self.__parent.add_child(self)
            
    def clone(self):
        c = super().clone()
        c.__samples = [v.clone() for v in self.samples]
        c.__scans = []
        c.__analyses = []
        c.__datastreams = []
        return c
    
    def parse(self, properties: dict):
        super().parse(properties)
        # Required fields
        self.__type = properties["type"]
        self.short_name = properties["short_name"]
        self.__context_id = properties["context"]
        
        # Optional fields
        self.__zone_id = properties.get("zone", "")            
        self.__factor_values = properties.get("factor_values", {})
        self.spatial_distribution = properties.get("spatial_distribution", "")
        self.description_file = properties.get("description_file", "")            
        self.__parent_id = properties.get("parent", "")            
        if "samples" in properties:
            self.__samples = self.factory.create_list("Sample", properties["samples"])
        else:
            self.__samples = []
        
    def serialize(self) -> dict:
        print("ObservationUnit.serialize: parent '%s'" % self.__parent_id)
        return { 'id': self.id,
                 'type': self.type,
                 'short_name': self.short_name,
                 'context': self.__context_id,
                 'zone': self.__zone_id,
                 'spatial_distribution': self.spatial_distribution,
                 'factor_values': self.factor_values,
                 'samples': self.samples,
                 'parent': self.__parent_id,
                 'description_file': self.description_file }

    
class BiologicalMaterial(BaseImpl, IBiologicalMaterial):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__description = ""
        self.__genus = ""
        self.__species = ""
        self.__intraspecific_name = ""
        self.__source_id = ""
        self.__source_doi = ""

    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def genus(self) -> str:
        return self.__genus

    @genus.setter
    def genus(self, value: str):
        self.__genus = value

    @property
    def species(self) -> str:
        return self.__species

    @species.setter
    def species(self, value: str):
        self.__species = value

    @property
    def intraspecific_name(self) -> str:
        return self.__intraspecific_name

    @intraspecific_name.setter
    def intraspecific_name(self, value: str):
        self.__intraspecific_name = value

    @property
    def source_id(self) -> str:
        return self.__source_id

    @source_id.setter
    def source_id(self, value: str):
        self.__source_id = value

    @property
    def source_doi(self) -> str:
        return self.__source_doi

    @source_doi.setter
    def source_doi(self, value: str):
        self.__source_doi = value

    ##
    
    def store(self) -> None:
        raise NotImplementedError()

    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.description = properties["description"]
        self.genus = properties["genus"]
        self.species = properties["species"]
        self.intraspecific_name = properties["intraspecific_name"]
        self.source_id = properties["source_id"]
        self.source_doi = properties["source_doi"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'description': self.description,
                 'genus': self.genus,
                 'species': self.species,
                 'intraspecific_name': self.intraspecific_name,
                 'source_id': self.source_id,
                 'source_doi': self.source_doi }

        
class Pose(BaseImpl, IPose):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)

    
class Observable(BaseImpl, IObservable):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__uri = ""
        self.__name = ""

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def name(self) -> str:
        return self.__name
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.__uri = properties["uri"]
        self.__name = properties["name"]

    def serialize(self) -> dict:
        return { "id": self.id, "uri": self.uri, "name": self.name }

        
class Unit(BaseImpl, IUnit):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__uri = ""
        self.__name = ""

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def name(self) -> str:
        return self.__name
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.__uri = properties["uri"]
        self.__name = properties["name"]

    def serialize(self) -> dict:
        return { "id": self.id, "uri": self.uri, "name": self.name }

        
class Note(BaseImpl, INote):
        
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__author = None
        self.__author_id = ""
        self.__observation_unit = None
        self.__observation_unit_id = ""
        self.__date = None
        self.__type = ""
        self.__text = ""

    @property
    def author(self) -> IPerson:
        return self.__author

    @author.setter
    def author(self, value: IPerson) -> None:
        self.__author = value
        self.__author_id = value.id

    @property
    def observation_unit(self) -> Any:
        return self.__observation_unit

    @observation_unit.setter
    def observation_unit(self, value: Any) -> None:
        self.__observation_unit = value
        self.__observation_unit_id = value.id

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def type(self) -> str:
        return self.__type
    
    @property
    def text(self) -> str:
        return self.__text

    def restore(self) -> None:
        self.__author = self.database.lookup(self.__author_id)
        self.__observation_unit = self.database.lookup(self.__observation_unit_id)
        self.__observation_unit.add_note(self)
        
    def parse(self, properties: dict):
        super().parse(properties)
        self.__author_id = properties["author"]
        self.__observation_unit_id = properties["observation_unit"]
        self.__date = dateutil.parser.parse(properties["date"])
        self.__type = properties["type"]
        self.__text = properties["text"]
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'author': self.__author_id,
                 'observation_unit': self.__observation_unit_id,
                 'date': self.date.isoformat(),
                 'type': self.type,
                 'text': self.text
        }

    
class DataStream(BaseImpl, IDataStream):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__observation_unit = None
        self.__observation_unit_id = ""
        self.__observable = None
        self.__unit = None
        self.__file = None
        self.__file_id = ""

    @property
    def observation_unit(self) -> Any:
        return self.__observation_unit

    @observation_unit.setter
    def observation_unit(self, value: Any) -> None:
        self.__observation_unit = value
        self.__observation_unit_id = value.id

    @property
    def file(self) -> IFile:
        return self.__file

    @file.setter
    def file(self, ifile: IFile) -> None:
        self.__file = ifile
        self.__file_id = ifile.id

    @property
    def observable(self) -> IObservable:
        return self.__observable

    @property
    def unit(self) -> IUnit:
        return self.__unit

    def get_values(self, db) -> List[dict]:
        return self.database.file_read_json(self.__file)
    
    def select(self, db, start_date: datetime = None,
               end_date: datetime = None) -> List[dict]:
        r = []
        start = None
        if start_date:
            start = start_date.isoformat()
        end = None
        if end_date:
            end = end_date.isoformat()
        for v in self.get_values(db):
            date = v["date"]
            if ((start == None or date >= start)
                and (end == None or date <= end)):
                r.append(v)
        return r

    ##
    
    def restore(self) -> None:
        self.__observation_unit = self.database.lookup(self.__observation_unit_id)
        self.__observation_unit.add_datastream(self)
        self.__file = self.database.get_file(self.__file_id)
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.__observation_unit_id = properties["observation_unit"]
        self.__observable = self.factory.create("Observable",
                                                properties["observable"])
        self.__unit = self.factory.create("Unit", properties["unit"])
        self.__file_id = properties["file"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'observation_unit': self.__observation_unit_id,
                 'observable': self.observable.serialize(),
                 'unit': self.unit.serialize(),
                 'file': self.__file_id
        }


class BoundingBox(BaseImpl, IBoundingBox):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__x = [0, 0]
        self.__y = [0, 0]
        self.__z = [0, 0]

    @property
    def x(self) -> List[float]:
        return self.__x
    
    @x.setter
    @abstractmethod
    def x(self, values: List[float]):
        self.__x = values
    
    @property
    def y(self) -> List[float]:
        return self.__y
    
    @y.setter
    @abstractmethod
    def y(self, values: List[float]):
        self.__y = values
        
    @property
    def z(self) -> List[float]:
        return self.__z
    
    @z.setter
    @abstractmethod
    def z(self, values: List[float]):
        self.__z = values

    ##

    def store(self) -> None:
        raise NotImplementedError()

    def parse(self, properties: dict):
        super().parse(properties)
        self.x = properties["x"]
        self.y = properties["y"]
        self.z = properties["z"]

    def serialize(self) -> dict:
        return { 'x': self.x,
                 'y': self.y,
                 'z': self.z }

    
class Scan(BaseImpl, IScan):
    
    def __init__(self, factory, database, classname): 
        BaseImpl.__init__(self, factory, database, classname)
        self.__observation_unit = None
        self.__observation_unit_id = ""
        self.__date = ""
        self.__people = []
        self.__person_ids = []
        self.__camera = None
        self.__camera_id = ""
        self.__scanning_device = None
        self.__scanning_device_id = ""
        self.__scan_path = ""
        self.__factor_values = {}
        self.__camera_poses = {}
        self.__bounding_box = None
        self.__images = []
        self.__analyses = []

    @property
    def observation_unit(self) -> str:
        return self.__observation_unit

    @observation_unit.setter
    def observation_unit(self, value: Any):
        self.__observation_unit = value
        self.__observation_unit_id = value.id

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        self.__date = value

    @property
    def operators(self) -> List[IPerson]:
        return self.__people

    @property
    def camera(self) -> str:
        return self.__camera

    @property
    def scanning_device(self) -> str:
        return self.__scanning_device

    @property
    def bounding_box(self) -> IBoundingBox:
        return self.__bounding_box

    @bounding_box.setter
    def bounding_box(self, value: IBoundingBox):
        self.__bounding_box = value

    @property
    def scan_path(self) -> str:
        return self.__scan_path
        
    def camera_pose_types(self) -> List[str]:
        pass

    def camera_poses(self, pose_type: str):
        pass
    
    def set_camera_pose(self, img_id: str, pose_type: str, pose: IPose) -> None:
        pass

    def get_camera_pose(self, img_id: str, pose_type: str) -> IPose:
        pass

    @property
    def factor_values(self) -> dict:
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, values: dict):
        self.__factor_values = values

    def set_factor_value(self, key: str, value: str):
        self.factor_values[key] = value

    @property
    def images(self) -> List[IFile]:
        return self.__images
            
    @property
    def analyses(self) -> List[IAnalysis]:
        return self.__analyses
        
    def add_analysis(self, analysis: IAnalysis):
        print("Scan.add_analysis")
        if find(analysis.id, self.analyses, "id") == None:
            self.analyses.append(analysis)
            analysis.scan = self

    ##

    def restore(self) -> None:
        self.__observation_unit = self.database.lookup(self.__observation_unit_id)
        self.__observation_unit.add_scan(self)
        self.__camera = self.database.lookup(self.__camera_id)
        self.__scanning_device = self.database.lookup(self.__scanning_device_id)
        self.__images = self.database.select_files("scan", self.id, None)

    def parse(self, properties: dict): 
        super().parse(properties)
        self.__observation_unit_id = properties["observation_unit"]
        self.__date = dateutil.parser.parse(properties["date"])
        self.__person_ids = properties["people"]
        self.__camera_id = properties["camera"]
        self.__scanning_device_id = properties["scanning_device"]
        self.__factor_values = properties["factor_values"]
        self.__scan_path = self.factory.create("ScanPath", properties["scan_path"])
        # TODO: load poses
        # TODO: load bounding box
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'observation_unit': self.__observation_unit_id,
                 'date': self.date.isoformat(),
                 'people': self.__person_ids,
                 'camera': self.__camera_id,
                 'scanning_device': self.__scanning_device_id,
                 'factor_values': self.factor_values,
                 'scan_path': self.scan_path
                 # POSES
                 # BOUNDING BOX
        }

        
class SoftwareModule(BaseImpl, ISoftwareModule):

    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__version = ""
        self.__repository = ""
        self.__branch = ""
        
    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, value: str):
        self.__version = value

    @property
    def repository(self) -> str:
        return self.__repository

    @repository.setter
    def repository(self, value: str):
        self.__repository = value

    @property
    def branch(self) -> str:
        return self.__branch

    @branch.setter
    def branch(self, value: str):
        self.__branch = value

    ##

    def store(self) -> None:
        raise NotImplementedError()

    def parse(self, properties: dict):
        super().parse(properties)
        self.version = properties["version"]
        self.repository = properties["repository"]
        self.branch = properties["branch"]
    
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'version': self.version,
                 'repository': self.repository,
                 'branch': self.branch }


class Parameters(BaseImpl, IParameters):

    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__values = {}

    def get_value(self, key: str) -> Any:
        return self.__values[key]

    def set_value(self, key: str, value: Any):
        self.__values[key] = value

    @property
    def values(self) -> dict:
        # the values are cloned to avoid modification without calling
        # set()
        return copy.deepcopy(self.__values) 

    ##

    def store(self) -> None:
        raise NotImplementedError()
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.__values = copy.deepcopy(properties)

    def serialize(self) -> dict:
        return self.__values


class ScanPath(BaseImpl, IScanPath):

    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__type = ""
        self.__parameters = None
        
    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def parameters(self) -> IParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: IParameters):
        self.__parameters = value

    ##

    def clone(self):
        c = super().clone()
        c.parameters = self.parameters.clone()
        return c
    
    def store(self) -> None:
        raise NotImplementedError()

    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.type = properties["type"]
        self.parameters = self.factory.create("Parameters",
                                              properties["parameters"])

    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'type': self.type,
                 'parameters': self.parameters.serialize() }

    
class Task(BaseImpl, ITask):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__software_module = None
        self.__parameters = None
        self.__state = ""
        self.__input_files = []
        self.__output_files = []
        self.log_file = ""
        
    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def software_module(self) -> ISoftwareModule:
        return self.__software_module

    @software_module.setter
    def software_module(self, value: ISoftwareModule):
        self.__software_module = value

    @property
    def parameters(self) -> IParameters:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: IParameters):
        self.__parameters = value
        
    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str):
        if not value in ITask.STATES:
            raise ValueError("Inavlid state value: %s", value)
        self.__state = value

    @property
    def input_files(self) -> List[str]:
        return self.__input_files

    def add_input_file(self, id: str):
        self.__input_files.append(id)

    @property
    def output_files(self) -> List[str]:
        return self.__output_files

    @output_files.setter
    def output_files(self, values: List[str]) -> None:
        self.__output_files = values

    def add_output_file(self, output_file: IFile):
        self.__output_files.append(output_file.id)
        
    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, value: str):
        self.__log_file = value

    ##

    def clone(self):
        c = super().clone()
        c.parameters = self.parameters.clone()
        c.software_module = self.software_module.clone()
        c.state = self.STATE_DEFINED
        c.__input_files = []
        c.output_files = [s for s in self.output_files]
        c.log_file = ""
        return c

    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.state = properties["state"]
        self.software_module = self.factory.create("SoftwareModule",
                                                   properties["software_module"])
        self.parameters = self.factory.create("Parameters",
                                              properties["parameters"])
        self.__input_files = properties["input_files"]
        #self.output_files = self.factory.create_list("File", properties["output_files"])
        self.output_files = properties["output_files"]
        self.log_file = properties["log_file"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'state': self.state,
                 'software_module': self.software_module.serialize(),
                 'parameters': self.parameters.serialize(),
                 'input_files': self.input_files,
                 'output_files': self.output_files,
                 'log_file': self.log_file }


class ObservedVariable(BaseImpl, IObservedVariable):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__name = ""
        self.__trait = ""
        self.__scale = ""
        self.__time_scale = ""
        
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        
    @property
    def trait(self) -> str:
        return self.__trait

    @trait.setter
    def trait(self, value: str):
        self.__trait = value
        
    @property
    def scale(self) -> str:
        return self.__scale

    @scale.setter
    def scale(self, value: str):
        self.__scale = value
        
    @property
    def time_scale(self) -> str:
        return self.__time_scale

    @time_scale.setter
    def time_scale(self, value: str):
        self.__time_scale = value    

    ##

    def parse(self, properties: dict):
        super().parse(properties)
        self.name = properties["name"]
        self.trait = properties["trait"]
        self.scale = properties["scale"]
        self.time_scale = properties["time_scale"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'name': self.name,
                 'trait': self.trait,
                 'scale': self.scale,
                 'time_scale': self.time_scale }

        
class Analysis(BaseImpl, IAnalysis):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
        self.__observation_unit = None
        self.__observation_unit_id = ""
        self.__scan = None
        self.__scan_id = ""
        self.__state = ""
        self.__observed_variables = []
        self.__tasks = []
        self.__results_file = None
    
    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
                
    @property
    def observation_unit(self) -> str:
        return self.__observation_unit

    @observation_unit.setter
    def observation_unit(self, value: Any) -> None:
        self.__observation_unit = value
        self.__observation_unit_id = value.id
        
    @property
    def scan(self) -> str:
        return self.__scan
    
    @scan.setter
    def scan(self, scan: IScan) -> None:
        self.__scan = scan
        self.__scan_id = scan.id
        print("Analysis.scan: scan_id='%s'" % self.__scan_id)
        
    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, value: str):
        self.__state = value

    @property
    def observed_variables(self) -> List[IObservedVariable]:
        return self.__observed_variables

    @observed_variables.setter
    def observed_variables(self, values: List[IObservedVariable]):
        self.__observed_variables = values

    @property
    def tasks(self) -> List[ITask]:
        return self.__tasks

    @tasks.setter
    def tasks(self, values: List[ITask]) -> None:
        self.__tasks = values

    def get_task_by_id(self, task_id: str) -> IFarm:
        return find(task_id, self.tasks, "id")
        
    def get_task_by_name(self, name: str) -> IFarm:
        return find(name, self.tasks, "short_name")
    
    def get_task(self, id_or_short_name: str) -> ITask:
        return (self.get_task_by_id(id_or_short_name)
                or self.get_task_by_name(id_or_short_name))

    @property
    def results_file(self) -> IFile:
        return self.__results_file

    ##

    def clone(self):
        c = super().clone()
        c.state = self.STATE_DEFINED
        c.__observed_variables = [v.clone() for v in self.observed_variables]
        c.__tasks = [v.clone() for v in self.tasks]
        return c
                    
    def restore(self) -> None:
        self.__observation_unit = self.database.lookup(self.__observation_unit_id)
        self.__observation_unit.add_analysis(self)
        print("Analysis.restore: scan_id='%s'" % self.__scan_id)
        if self.__scan_id:
            self.__scan = self.database.lookup(self.__scan_id)
            self.__scan.add_analysis(self)
        files = self.database.select_files(self.short_name, self.id, "results")
        if len(files) >= 1:
            self.__results_file = files[0]
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.__short_name = properties["short_name"]
        self.__name = properties["name"]
        self.__description = properties["description"]
        self.__observation_unit_id = properties.get("observation_unit", "")
        self.__scan_id = properties.get("scan", "")
        print("Analysis.parse: scan_id='%s'" % self.__scan_id)
        self.__state = properties["state"]
        self.observed_variables = self.factory.create_list("ObservedVariable",
                                                           properties["observed_variables"])
        self.tasks = self.factory.create_list("Task", properties["tasks"])

    def serialize(self) -> dict:
        print("Analysis.serialize: scan_id='%s'" % self.__scan_id)
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'observation_unit': self.__observation_unit_id,
                 'scan': self.__scan_id,
                 'state': self.state,
                 'observed_variables': self.observed_variables,
                 'tasks': self.tasks }


class ExperimentalFactor(BaseImpl, IExperimentalFactor):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__description = ""
        self.__values = ""
   
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value
        
    @property
    def values(self) -> List[str]:
        return self.__values

    @values.setter
    def values(self, values: List[str]):
        self.__values = values

    ##

    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.description = properties["description"]
        self.values = properties["values"]
   
    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'description': self.description,
                 'values': self.values }


class Study(BaseImpl, IStudy):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__investigation = None
        self.__investigation_id = ""
        self.__title = ""
        self.__description = ""
        self.__people = []
        self.__cameras = []
        self.__scanning_devices = []
        self.__files = []
        self.__scans = []
        self.__analyses = []
        self.__experimental_factors = []
        self.__observation_units = []
        self.__scan_paths = []
        
    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value
        
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def investigation(self) -> Any:
        return self.__investigation

    @investigation.setter
    def investigation(self, value: Any):
        self.__investigation_id = value.id
        self.__investigation = value

    @property
    def people(self) -> List[IPerson]:
        return self.__people

    @people.setter
    def people(self, values: List[IPerson]):
        self.__people = values

    @property
    def cameras(self) -> List[ICamera]:
        return self.__cameras

    @cameras.setter
    def cameras(self, values: List[ICamera]):
        self.__cameras = values

    @property
    def scanning_devices(self) -> List[ScanningDevice]:
        return self.__scanning_devices

    @scanning_devices.setter
    def scanning_devices(self, values: List[ICamera]):
        self.__scanning_devices = values

    @property
    def files(self) -> List[IFile]:
        return self.__files

    @files.setter
    def files(self, values: List[ICamera]):
        self.__files = values

    @property
    def scans(self) -> List[IScan]:
        return self.__scans

    @scans.setter
    def scans(self, values: List[IScan]):
        self.__scans = values

    @property
    def analyses(self) -> List[IAnalysis]:
        return self.__analyses

    @analyses.setter
    def analyses(self, values: List[IScan]):
        self.__analyses = values

    @property
    def experimental_factors(self) -> List[IExperimentalFactor]:
        return self.__experimental_factors

    @experimental_factors.setter
    def experimental_factors(self, values: List[IExperimentalFactor]):
        self.__experimental_factors = values

    @property
    def observation_units(self) -> List[IObservationUnit]:
        return self.__observation_units

    @observation_units.setter
    def observation_units(self, values: List[IObservationUnit]):
        self.__observation_units = values

    @property
    def scan_paths(self) -> List[IScanPath]:
        return self.__scan_paths

    @scan_paths.setter
    def scan_paths(self, values: List[IScanPath]):
        self.__scan_paths = values

    ##
    
    def clone(self):
        c = super().clone()
        c.__people = [p.clone for p in self.people]
        c.__cameras = [c.clone for c in self.cameras]
        c.__scanning_devices = [s.clone for s in self.scanning_devices]
        c.__scan_paths = [s.clone for s in self.scan_paths]
        c.__files = []
        c.__scans = []
        c.__analyses = []
        c.__observation_units = []
        return c
            
    def restore(self) -> None:
        self.__investigation = self.database.lookup(self.__investigation_id)

    def parse(self, properties: dict):
        super().parse(properties)
        self.__title = properties["title"]
        self.__description = properties["description"]
        self.__investigation_id = properties["investigation"]
        self.people = self.factory.create_list("Person", properties["people"])
        self.cameras = self.factory.create_list("Camera", properties["cameras"])
        self.scanning_devices = self.factory.create_list("ScanningDevice",
                                                         properties["scanning_devices"])
        self.files = self.factory.create_list("File", properties["files"])
        for f in self.files:
            f.parent = self
        self.analyses = self.factory.create_list("Analysis", properties["analyses"])
        for analysis in self.analyses:
            analysis.parent = self
            
        self.experimental_factors = self.factory.create_list("ExperimentalFactor",
                                                             properties["experimental_factors"])
        self.observation_units = self.factory.create_list("ObservationUnit",
                                                          properties["observation_units"])
        self.scan_paths = self.factory.create_list("ScanPath", properties["scan_paths"])
        self.scans = self.factory.create_list("Scan", properties["scans"])
        for scan in self.scans:
            scan.parent = self
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'title': self.title,
                 'description': self.description,
                 'investigation': self.__investigation_id,
                 'people': self.people,
                 'cameras': self.cameras,
                 'scanning_devices': self.scanning_devices,
                 'files': self.files,
                 'scans': self.scans,
                 'analyses': self.analyses,
                 'experimental_factors': self.experimental_factors,
                 'observation_units': self.observation_units,
                 'scan_paths': self.scan_paths }

    def validate_person_name(self, value: str):
        if not find(value, self.people, "short_name"):
            raise ValueError("The person %s isn't listed in the study, yet" % value)
        
    def validate_observation_unit_id(self, value: str):
        if not find(value, self.observation_units, "id"):
            raise ValueError("The observationd unit %s was not found in the study"
                             % value)

    def __get_experimental_factor(self, name: str):
        for factor in self.experimental_factors:
            if factor.short_name == name:
                return factor
        return None

    def __get_factor_values(self, name: str):
        factor = self.__get_experimental_factor(name)
        if not factor:
            return None
        else:
            return factor.values
    
    def validate_camera_name(self, value: str) -> str:
        r = value
        if not value:
            if len(self.cameras) == 1:
                r = self.cameras[0].short_name
            else:
                raise ValueError("Missing the name of the camera")
        else:
            if not find(value, self.cameras, "short_name"):
                raise ValueError("The camera %s is not used in the study" % value)
        return r

    def validate_scanning_device_name(self, value: str) -> str:
        r = value
        if not value:
            if len(self.scanning_devices) == 1:
                r = self.scanning_devices[0].short_name
            else:
                raise ValueError("Missing the name of the scanning device")
        else:
            if not find(value, self.scanning_devices, "short_name"):
                raise ValueError("The scanning device %s is not used in the study"
                                 % value)
        return r
        
    def validate_scan_path_name(self, value: str) -> str:
        r = value
        if not value:
            if len(self.scan_paths) == 1:
                r = self.scan_paths[0].short_name
            else:
                raise ValueError("Missing the name of the scan path")
        else:
            if not find(value, self.scan_paths, "short_name"):
                raise ValueError("The scan path %s is not used in the study"
                                 % value)
        return r
    
    def validate_factor_values(self, values: dict, observation_unit: IObservationUnit):
        factor_names = [v.short_name for v in self.experimental_factors]
        given_factors = { **values, **observation_unit.factor_values }
        for factor_name in factor_names:
            if not factor_name in given_factors:
                raise ValueError("Missing factor value: %s" % factor_name)
            given_value = given_factors[factor_name]
            valid_values = self.__get_factor_values(factor_name)
            found_value = False
            for possible_value in valid_values:
                if given_value == possible_value:
                    found_value = True
                    break
            if not found_value:
                raise ValueError("Invalid value for factor %s: %s"
                                 % (factor_name, given_value))
                
    def new_scan(self, db, **kwargs) -> IScan:
        
        person_names = kwargs["person_names"]
        for name in person_names:
            self.validate_person_name(name)
            
        camera_name = None
        if "camera_name" in kwargs:
            camera_name = kwargs["camera_name"]
        camera_name = self.validate_camera_name(camera_name)

        scanning_device_name = None
        if "scanning_device_name" in kwargs:
            scanning_device_name = kwargs["scanning_device_name"]
        scanning_device_name = self.validate_scanning_device_name(scanning_device_name)
        
        observation_unit_id = kwargs["observation_unit_id"]
        self.validate_observation_unit_id(observation_unit_id)

        observation_unit = find(observation_unit_id, self.observation_units, "id")

        scan_path_name = None
        if "scan_path_name" in kwargs:
            scan_path_name = kwargs["scan_path_name"]
        scan_path_name = self.validate_scan_path_name(scan_path_name)

        factor_values = {}
        if "factor_values" in kwargs:
            factor_values = kwargs["factor_values"]
        self.validate_factor_values(factor_values, observation_unit)
        
        scan = self.factory.create("Scan", {
            "date": current_date().isoformat(),
            "person_names": person_names,
            "camera_name": camera_name,
            "scanning_device_name": scanning_device_name,
            "observation_unit_id": observation_unit_id,
            "scan_path_name": scan_path_name,
            "factor_values": factor_values,
            "camera_poses": []
        })
        
        self.add_scan(scan)
        scan.parent = self
        return scan

    def clone_scan(self, scan: IScan) -> IScan:
        newscan = scan.clone()
        newscan.id = new_id()
        newscan.date = current_date()
        self.add_scan(newscan)
        return newscan


        
class Investigation(BaseImpl, IInvestigation):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__title = ""
        self.__description = ""
        self.__license = ""
        self.__people = []
        self.__studies = []
        
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def license(self) -> str:
        return self.__license

    @license.setter
    def license(self, value: str):
        self.__license = value

    @property
    def publications(self) -> List[str]:
        return self.__publications

    def add_publication(self, ref: str):
        self.__publications.append(ref)
    
    @property
    def people(self) -> List[IPerson]:
        return self.__people
    
    @people.setter
    def people(self, value: List[IPerson]):
        self.__people = value

    def add_person(self, person: IPerson):
        self.people.append(person)

    @property
    def studies(self) -> List[IStudy]:
        return self.__studies

    @studies.setter
    def studies(self, value: List[IStudy]):
        self.__studies = value
        
    def add_study(self, study: IStudy):
        study.parent = self
        self.studies.append(study)

    ## 

    def clone(self):
        c = super().clone()
        c.__publications = []
        c.__people = []
        return c
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.title = properties["title"]
        self.description = properties["description"]
        self.license = properties["license"]
        self.people = self.factory.create_list("Person", properties["people"])
        self.studies = self.factory.create_list("Study", properties["studies"])
        for study in self.studies:
            study.parent = self
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'title': self.title,
                 'description': self.description,
                 'license': self.license,
                 'people': self.people,
                 'studies': self.studies }

    
class Zone(BaseImpl, IZone):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__id = ""
        self.__farm = None
        self.__farm_id = ""
        self.__short_name = ""
        self.__observation_units = []
    
    @property
    def farm(self) -> Any:
        return self.__farm

    @farm.setter
    def farm(self, value: Any):
        self.__farm_id = value.id
        self.__farm = value
        
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value
        
    @property
    def observation_units(self) -> List[IObservationUnit]:
        return self.__observation_units

    def add_observation_unit(self, obj: IObservationUnit):
        if find(obj.id, self.observation_units, "id") == None:
            self.__observation_units.append(obj)

    def get_observation_unit(self, oid: str, otype: str) -> IObservationUnit:
        r = None
        for obj in self.observation_units:
            if ((not oid or obj.id == oid)
                and (not otype or obj.type == otype)):
                r = obj
                break        
        return r

    ##
    
    def restore(self) -> None:
        self.__farm = self.database.lookup(self.__farm_id)
        self.__farm.add_zone(self)

    def parse(self, properties: dict):
        super().parse(properties)
        self.__farm_id = properties["farm"]
        self.__short_name = properties["short_name"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'farm': self.__farm_id,
                 'short_name': self.short_name }

        

class Farm(BaseImpl, IFarm):
    
    def __init__(self, factory, database, classname):
        BaseImpl.__init__(self, factory, database, classname)
        self.__short_name = ""
        self.__description = ""
        self.__address = ""
        self.__country = ""
        self.__photo = None
        self.__photo_id = ""
        self.__location = [0, 0]
        self.__license = ""
        self.__people = []
        self.__person_ids = []
        self.__cameras = []
        self.__scanning_devices = []
        self.__scan_paths = []
        self.__zones = []
        self.__observation_units = []

    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        self.__address = value

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str):
        self.__country = value

    @property
    def photo(self) -> IFile:
        return self.__photo

    @photo.setter
    def photo(self, ifile: IFile) -> None:
        self.__photo = ifile
        self.__photo_id = ifile.id

    @property
    def location(self) -> List[float]:
        return self.__location

    @property
    def license(self) -> str:
        return self.__license

    @license.setter
    def license(self, value: str):
        self.__license = value
    
    @property
    def people(self) -> List[IPerson]:
        return self.__people
    
    def add_person(self, person: IPerson):
        self.__people.append(person)
        self.__person_ids.append(person.id)

    def get_person(self, id_or_name: str):
        return (find(id_or_name, self.people, "id")
                or find(id_or_name, self.people, "short_name"))
    
    @property
    def cameras(self) -> List[ICamera]:
        return self.__cameras

    @cameras.setter
    def cameras(self, values: List[ICamera]):
        self.__cameras = values

    def add_camera(self, camera: ICamera):
        if find(camera.id, self.cameras, "id") == None:
            self.cameras.append(camera)
            camera.owner = self

    def get_camera(self, id_or_name: str):
        return (find(id_or_name, self.cameras, "id")
                or find(id_or_name, self.cameras, "short_name"))
            
    @property
    def scanning_devices(self) -> List[ScanningDevice]:
        return self.__scanning_devices
    
    def add_scanning_device(self, device: IScanningDevice):
        if find(device.id, self.scanning_devices, "id") == None:
            self.scanning_devices.append(device)
            device.owner = self

    def get_scanning_device(self, id_or_name: str):
        return (find(id_or_name, self.scanning_devices, "id")
                or find(id_or_name, self.scanning_devices, "short_name"))
            
    @property
    def scan_paths(self) -> List[IScanPath]:
        return self.__scan_paths
    
    def add_scan_path(self, value: IScanPath):
        self.scan_paths.append(value)
        
    def get_scan_path(self, id_or_name: str):
        return (find(id_or_name, self.scanning_devices, "id")
                or find(id_or_name, self.scan_paths, "short_name"))

    @property
    def zones(self) -> List[str]:
        return self.__zones

    def add_zone(self, zone: IZone):
        if find(zone.id, self.zones, "id") == None:
            self.zones.append(zone)
            zone.farm = self
        
    @property
    def observation_units(self) -> List[IObservationUnit]:
        return self.__observation_units

    def add_observation_unit(self, obj: IObservationUnit):
        if find(obj.id, self.observation_units, "id") == None:
            obj.context = self
            self.__observation_units.append(obj)

    def get_observation_unit(self, oid: str, otype: str = "") -> IObservationUnit:
        r = None
        for obj in self.observation_units:
            if ((not oid or obj.id == oid or obj.short_name == oid)
                and (not otype or obj.type == otype)):
                r = obj
                break        
        return r
        
    ##

    def clone(self):
        c = super().clone()
        c.__photo = None
        c.__photo_id = ""
        c.__people = []
        c.__person_ids = []
        c.__cameras = [s.clone for s in self.__cameras]
        c.__scanning_devices = [s.clone for s in self.__scanning_devices]
        c.__scan_paths = [s.clone for s in self.scan_paths]
        c.__zones = []
        return c

    def restore(self) -> None:
        self.__people = lookup_id_list(self.database, self.__person_ids)
        if self.__photo_id:
            self.__photo = self.database.get_file(self.__photo_id)
    
    def parse(self, properties: dict):
        super().parse(properties)
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.address = properties["address"]
        self.country = properties["country"]
        self.license = properties["license"]

        self.__photo_id = properties.get("photo", "")
        self.__location = properties.get("location", [0,0])

        if "people" in properties:
            self.__person_ids = properties["people"]
            
        if "scan_paths" in properties:
            self.__scan_paths = self.factory.create_list("ScanPath",
                                                         properties["scan_paths"])
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'address': self.address,
                 'country': self.country,
                 'photo': self.__photo_id,
                 'location': self.location,
                 'license': self.license,
                 'people': self.__person_ids,
                 'scan_paths': self.scan_paths,
        }


class DefaultFactory(IFactory):
    def __init__(self, database: IDatabase):
        self.__database = database
    
    def create(self, classname: str, properties: dict) -> Any:
        switcher = {
            "File": File,
            "Person": Person,
            "Camera": Camera,
            "ScanningDevice": ScanningDevice,
            "BiologicalMaterial": BiologicalMaterial,
            "Pose": Pose,
            "Scan": Scan,
            "SoftwareModule": SoftwareModule,
            "Parameters": Parameters,
            "Task": Task,
            "ObservedVariable": ObservedVariable,
            "Analysis": Analysis,
            "Study": Study,
            "Investigation": Investigation,
            "Zone": Zone,
            "Farm": Farm,
            "ExperimentalFactor": ExperimentalFactor,
            "ObservationUnit": ObservationUnit,
            "Sample": Sample,
            "ScanPath": ScanPath,
            "Unit": Unit,
            "Observable": Observable,
            "DataStream": DataStream,
            "Note": Note
        }
        constructor = switcher.get(classname)
        if not constructor:
            raise ValueError("Can't find constructor for %s" % classname)
        obj = constructor(self, self.__database, classname)
        obj.parse(properties)
        return obj
    
    def create_list(self, classname: str, properties: List[dict]) -> List[Any]:
        array = []
        for p in properties:
            obj = self.create(classname, p)
            array.append(obj)
        return array
