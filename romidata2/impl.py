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
from datetime import datetime

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

def new_id(length: int = 8) -> str:
    """Generates a new random ID with a given length."""
    return ''.join([random.choice(string.ascii_lowercase 
                                  + string.digits)
                    for n in range(length)])

def current_date() -> datetime:
    """Generates a datetime object with the current date. The timezone will be set."""
    tz = get_localzone()
    return tz.localize(datetime.now())

    
class File(IFile):
    def __init__(self):
        self.__parent = None
        self.__id = ""
        self.__source_name = ""
        self.__source_id = ""
        self.__short_name = ""
        self.__path = ""
        self.__mimetype = ""
        
    @property
    def parent(self) -> Any:
        return self.__parent

    @parent.setter
    def parent(self, value: Any):
        self.__parent = value
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

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
        
    def parse(self, factory: IFactory, properties: dict):
        self.__id = properties["id"]
        self.__source_name = properties["source_name"]
        self.__source_id = properties["source_id"]
        self.__short_name = properties["short_name"]
        self.__path = properties["path"]
        self.__mimetype = properties["mimetype"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'source_name': self.source_name,
                 'source_id': self.source_id,
                 'short_name': self.short_name,
                 'path': self.path,
                 'mimetype': self.mimetype }



class Person(IPerson):
    def __init__(self):
        self.__id = ""
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
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, value: str):
        self.__role = value

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
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

    
class Camera(ICamera):
    def __init__(self):
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
        self.__lens = ""
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

    def parse(self, factory: IFactory, properties: dict):
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.lens = properties["lens"]
        self.software_module = factory.create("SoftwareModule",
                                              properties["software_module"])
        self.parameters = factory.create("Parameters",
                                         properties["parameters"])

    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'lens': self.lens,
                 'software_module': self.software_module,
                 'parameters': self.parameters }


class ScanningDevice(IScanningDevice):
    def __init__(self):
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
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

    def parse(self, factory: IFactory, properties: dict):
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.software_module = factory.create("SoftwareModule",
                                              properties["software_module"])
        self.parameters = factory.create("Parameters", properties["parameters"])
        
    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'software_module': self.software_module,
                 'parameters': self.parameters }

        
class Sample(ISample):
    def __init__(self):
        self.__id = ""
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
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
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

    
class ObservationUnit(IObservationUnit):
    def __init__(self):
        self.__id = ""
        self.__type = ""
        self.__spatial_distribution = ""
        self.__factor_values = {}
        self.__samples = []
        self.__description_file = ""

    def clone(self):
        c = copy.deepcopy(self)
        c.__samples = [v.clone() for v in self.samples]
        return c
        
    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
    
    @property
    def spatial_distribution(self) -> str:
        return self.__spatial_distribution

    @spatial_distribution.setter
    def spatial_distribution(self, value: str):
        self.__spatial_distribution = value

    @property
    def factor_values(self) -> dict:
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, values: dict):
        self.__factor_values = values

    @property
    def samples(self) -> List[ISample]:
        return self.__samples

    @samples.setter
    def samples(self, values: List[ISample]):
        self.__samples = values
        
    @property
    def description_file(self) -> str:
        return self.__description_file

    @description_file.setter
    def description_file(self, value: str):
        self.__description_file = value

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.type = properties["type"]
        self.spatial_distribution = properties["spatial_distribution"]
        self.factor_values = properties["factor_values"]
        if "description_file" in properties:
            self.description_file = properties["description_file"]
        else:
            self.description_file = ""
        self.samples = factory.create_list("Sample", properties["samples"])
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'type': self.type,
                 'spatial_distribution': self.spatial_distribution,
                 'factor_values': self.factor_values,
                 'samples': self.samples,
                 'description_file': self.description_file }

    
class BiologicalMaterial(IBiologicalMaterial):
    def __init__(self):
        self.__id = ""
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
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
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

        
class Pose(IPose):
    def __init__(self):
        pass
    
    def parse(self, factory: IFactory, properties: dict):
        pass

    
class BoundingBox(IBoundingBox):
    def __init__(self):
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
    
    def parse(self, factory: IFactory, properties: dict):
        self.x = properties["x"]
        self.y = properties["y"]
        self.z = properties["z"]

    def serialize(self) -> dict:
        return { 'x': self.x,
                 'y': self.y,
                 'z': self.z }

    
class Scan(IScan):
    def __init__(self): 
        self.__parent = None
        self.__id = ""
        self.__date = ""
        self.__person_names = []
        self.__camera_name = ""
        self.__scanning_device_name = ""
        self.__observation_unit = ""
        self.__factor_values = {}
        self.__camera_poses = {}
        self.__bounding_box = None
        self.__scan_path_name = None
        
    @property
    def id(self) -> str:
        return self.__id
        
    @id.setter
    def id(self, value: str):
        self.__id = value
        
    @property
    def parent(self):
        return self.__parent
        
    @parent.setter
    def parent(self, value: Any): # value: Study... forward class declaration in Python?
        self.__parent = value

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        self.__date = value

    @property
    def person_names(self) -> List[str]:
        return self.__person_names

    @person_names.setter
    def person_names(self, values: List[str]):
        self.__person_names = values

    @property
    def camera_name(self) -> str:
        return self.__camera_name

    @camera_name.setter
    def camera_name(self, value: str):
        self.__camera_name = value

    @property
    def scanning_device_name(self) -> str:
        return self.__scanning_device_name

    @scanning_device_name.setter
    def scanning_device_name(self, value: str):
        self.__scanning_device_name = value

    @property
    def observation_unit_id(self) -> str:
        return self.__observation_unit_id

    @observation_unit_id.setter
    def observation_unit_id(self, value: str):
        if self.parent: self.parent.validate_observation_unit_id(value)
        self.__observation_unit_id = value

    @property
    def bounding_box(self) -> IBoundingBox:
        return self.__bounding_box

    @bounding_box.setter
    def bounding_box(self, value: IBoundingBox):
        self.__bounding_box = value

    @property
    def scan_path_name(self) -> str:
        return self.__scan_path

    @scan_path_name.setter
    def scan_path_name(self, value: str):
        self.__scan_path = value
        
    def camera_pose_types(self) -> List[str]:
        pass

    def camera_poses(self, pose_type: str):
        pass
    
    def set_camera_pose(self, img_id: str, pose_type: str, pose: IPose) -> None:
        pass

    def get_camera_pose(self, img_id: str, pose_type: str) -> IPose:
        pass

    @property
    def images(self):
        return self.parent.get_files_by_source("scan", self.id, "")

    @property
    def factor_values(self) -> dict:
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, values: dict):
        self.__factor_values = values

    def set_factor_value(self, key: str, value: str):
        self.factor_values[key] = value

    def parse(self, factory: IFactory, properties: dict): 
        self.id = properties["id"]
        self.date = dateutil.parser.parse(properties["date"])
        self.person_names = properties["person_names"]
        self.camera_name = properties["camera_name"]
        self.scanning_device_name = properties["scanning_device_name"]
        self.observation_unit_id = properties["observation_unit_id"]
        self.factor_values = properties["factor_values"]
        self.scan_path_name = properties["scan_path_name"]
        # TODO: load poses
        # TODO: load bounding box
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'date': self.date.isoformat(),
                 'person_names': self.person_names,
                 'camera_name': self.camera_name,
                 'scanning_device_name': self.scanning_device_name,
                 'observation_unit_id': self.observation_unit_id,
                 'factor_values': self.factor_values,
                 'scan_path_name': self.scan_path_name
                 # POSES
                 # BOUNDING BOX
        }

        
class SoftwareModule(ISoftwareModule):
    def __init__(self):
        self.__id = ""
        self.__version = ""
        self.__repository = ""
        self.__branch = ""

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.version = properties["version"]
        self.repository = properties["repository"]
        self.branch = properties["branch"]
    
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'version': self.version,
                 'repository': self.repository,
                 'branch': self.branch }


class Parameters(IParameters):
    def __init__(self):
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
    
    def parse(self, factory: IFactory, properties: dict):
        self.__values = copy.deepcopy(properties)

    def serialize(self) -> dict:
        return self.__values


class ScanPath(IScanPath):
    def __init__(self):
        self.__short_name = ""
        self.__type = ""
        self.__parameters = None

    def clone(self):
        c = copy.copy(self)
        c.parameters = self.parameters.clone()
        return c
        
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
    
    def parse(self, factory: IFactory, properties: dict):
        self.short_name = properties["short_name"]
        self.type = properties["type"]
        self.parameters = factory.create("Parameters",
                                         properties["parameters"])

    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'type': self.type,
                 'parameters': self.parameters }

    
class Task(ITask):
    
    def __init__(self):
        self.__id = ""
        self.__short_name = ""
        self.__software_module = None
        self.__parameters = None
        self.__state = ""
        self.__input_files = []
        self.__output_files = []
        self.log_file = ""

    def clone(self):
        c = copy.copy(self)
        c.id = new_id()
        c.parameters = self.parameters.clone()
        c.software_module = self.software_module.clone()
        c.state = self.STATE_DEFINED
        c.__input_files = []
        c.output_files = [s for s in self.output_files]
        c.log_file = ""
        return c
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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
        self.parent.add_file(output_file)
        self.__output_files.append(output_file.id)
        
    @property
    def log_file(self):
        return self.__log_file

    @log_file.setter
    def log_file(self, value: str):
        self.__log_file = value
    
    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.short_name = properties["short_name"]
        self.state = properties["state"]
        self.software_module = factory.create("SoftwareModule",
                                              properties["software_module"])
        self.parameters = factory.create("Parameters",
                                         properties["parameters"])
        self.__input_files = properties["input_files"]
        #self.output_files = factory.create_list("File", properties["output_files"])
        self.output_files = properties["output_files"]
        self.log_file = properties["log_file"]

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'state': self.state,
                 'software_module': self.software_module,
                 'parameters': self.parameters,
                 'input_files': self.input_files,
                 'output_files': self.output_files,
                 'log_file': self.log_file }


class ObservedVariable(IObservedVariable):
    def __init__(self):
        self.__id = ""
        self.__name = ""
        self.__trait = ""
        self.__scale = ""
        self.__time_scale = ""
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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
        
    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
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

        
class Analysis(IAnalysis):
    
    def __init__(self):
        self.__parent = None
        self.__id = new_id()
        self.__short_name = ""
        self.__name = ""
        self.__description = ""
        self.__scan_id = ""
        self.__state = ""
        self.__observed_variables = []
        self.__tasks = []

    def clone(self):
        c = copy.copy(self)
        c.id = new_id()
        c.state = self.STATE_DEFINED
        c.__observed_variables = [v.clone() for v in self.observed_variables]
        c.__tasks = [v.clone() for v in self.tasks]
        return c
        
    @property
    def parent(self):
        return self.__parent
        
    @parent.setter
    def parent(self, value: Any): # value: Study... forward class declaration in Python?
        self.__parent = value
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
    
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
    def scan_id(self) -> str:
        return self.__scan_id

    @scan_id.setter
    def scan_id(self, value: str):
        self.__scan_id = value
        
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
        return self.find(task_id, self.tasks, "id")
        
    def get_task_by_name(self, name: str) -> IFarm:
        return self.find(name, self.tasks, "short_name")
    
    def get_task(self, id_or_short_name: str) -> ITask:
        return (self.get_task_by_id(id_or_short_name)
                or self.get_task_by_name(id_or_short_name))

    @property
    def results_file(self) -> IFile:
        r = None
        files = self.parent.get_files_by_source(self.short_name, self.id, "results")
        if len(files) >= 1:
            r = files[0]
        return r
        
    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.scan_id = properties["scan_id"]
        self.state = properties["state"]
        self.observed_variables = factory.create_list("ObservedVariable",
                                                      properties["observed_variables"])
        self.tasks = factory.create_list("Task", properties["tasks"])
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'scan_id': self.scan_id,
                 'state': self.state,
                 'observed_variables': self.observed_variables,
                 'tasks': self.tasks }


class ExperimentalFactor(IExperimentalFactor):
    def __init__(self):
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

    def parse(self, factory: IFactory, properties: dict):
        self.short_name = properties["short_name"]
        self.description = properties["description"]
        self.values = properties["values"]
   
    def serialize(self) -> dict:
        return { 'short_name': self.short_name,
                 'description': self.description,
                 'values': self.values }


class Study(IStudy):
    def __init__(self):
        self.__factory = None
        self.__parent = None
        self.__id = ""
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

    def clone(self):
        c = copy.copy(self)
        c.id = new_id()
        c.__parent = None
        c.__people = [p.clone for p in self.people]
        c.__cameras = [c.clone for c in self.cameras]
        c.__scanning_devices = [s.clone for s in self.scanning_devices]
        c.__scan_paths = [s.clone for s in self.scan_paths]
        c.__files = []
        c.__scans = []
        c.__analyses = []
        c.__observation_units = []
        return c
        
    @property
    def parent(self) -> Any:   # FIXME: forward declaration of classes?
        return self.__parent

    @parent.setter
    def parent(self, value: Any):
        self.__parent = value
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
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

    def parse(self, factory: IFactory, properties: dict):
        self.__factory = factory
        self.__id = properties["id"]
        self.__title = properties["title"]
        self.__description = properties["description"]
        self.people = factory.create_list("Person", properties["people"])
        self.cameras = factory.create_list("Camera", properties["cameras"])
        self.scanning_devices = factory.create_list("ScanningDevice",
                                                    properties["scanning_devices"])
        self.files = factory.create_list("File", properties["files"])
        for f in self.files:
            f.parent = self
        self.analyses = factory.create_list("Analysis", properties["analyses"])
        for analysis in self.analyses:
            analysis.parent = self
            
        self.experimental_factors = factory.create_list("ExperimentalFactor",
                                                        properties["experimental_factors"])
        self.observation_units = factory.create_list("ObservationUnit",
                                                     properties["observation_units"])
        self.scan_paths = factory.create_list("ScanPath",
                                              properties["scan_paths"])
        self.scans = factory.create_list("Scan", properties["scans"])
        for scan in self.scans:
            scan.parent = self

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'title': self.title,
                 'description': self.description,
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
        if not self.find(value, self.people, "short_name"):
            raise ValueError("The person %s isn't listed in the study, yet" % value)
        
    def validate_observation_unit_id(self, value: str):
        if not self.find(value, self.observation_units, "id"):
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
                
    def new_scan(self, **kwargs) -> IScan:
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

        observation_unit = self.find(observation_unit_id, self.observation_units, "id")

        scan_path_name = None
        if "scan_path_name" in kwargs:
            scan_path_name = kwargs["scan_path_name"]
        scan_path_name = self.validate_scan_path_name(scan_path_name)

        factor_values = {}
        if "factor_values" in kwargs:
            factor_values = kwargs["factor_values"]
        self.validate_factor_values(factor_values, observation_unit)
        
        scan = self.__factory.create("Scan",
                                     {"id": new_id(),
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


        
class Investigation(IInvestigation):
    def __init__(self):
        self.__id = ""
        self.__short_name = ""
        self.__title = ""
        self.__description = ""
        self.__license = ""
        self.__people = []
        self.__studies = []

    def clone(self):
        c = copy.copy(self)
        c.__id = new_id()
        c.__publications = []
        c.__people = []
        return c
        
    @property
    def id(self):
        return self.__id
        
    @id.setter
    def id(self, value: str):
        self.__id = value

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
        if not person:
            raise Error() 
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

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.short_name = properties["short_name"]
        self.title = properties["title"]
        self.description = properties["description"]
        self.license = properties["license"]
        self.people = factory.create_list("Person", properties["people"])
        self.studies = factory.create_list("Study", properties["studies"])
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


    
class Zone(IZone):
    def __init__(self):
        self.__factory = None
        self.__parent = None
        self.__id = ""
        self.__short_name = ""
        self.__scan_paths = []
        self.__files = []
        self.__scans = []
        self.__analyses = []

    def clone(self):
        c = copy.copy(self)
        c.id = new_id()
        c.__parent = None
        c.__scan_paths = [p.clone for p in self.scan_paths]
        c.__files = []
        c.__scans = []
        c.__analyses = []
        return c
    
    @property
    def parent(self) -> Any:   # FIXME: forward declaration of classes?
        return self.__parent

    @parent.setter
    def parent(self, value: Any):
        self.__parent = value
        
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value
        
    @property
    def short_name(self) -> str:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self.__short_name = value

    @property
    def cameras(self) -> List[ICamera]:
        if self.parent != None:
            return self.parent.cameras
        else:
            return []

    @property
    def scanning_devices(self) -> List[ScanningDevice]:
        if self.parent != None:
            return self.parent.scanning_devices
        else:
            return []

    @property
    def scan_paths(self) -> List[IScanPath]:
        return self.__scan_paths

    @scan_paths.setter
    def scan_paths(self, values: List[IScanPath]):
        self.__scan_paths = values

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

    def parse(self, factory: IFactory, properties: dict):
        self.__factory = factory
        self.__id = properties["id"]
        self.__short_name = properties["short_name"]
        self.scan_paths = factory.create_list("ScanPath", properties["scan_paths"])
        self.files = factory.create_list("File", properties["files"])
        for f in self.files:
            f.parent = self
        self.analyses = factory.create_list("Analysis", properties["analyses"])
        for analysis in self.analyses:
            analysis.parent = self
        self.scans = factory.create_list("Scan", properties["scans"])
        for scan in self.scans:
            scan.parent = self

    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'scan_paths': self.scan_paths,
                 'files': self.files,
                 'scans': self.scans,
                 'analyses': self.analyses }
                
    def new_scan(self, **kwargs) -> IScan:
            
        camera_name = None
        if "camera_name" in kwargs:
            camera_name = kwargs["camera_name"]
        camera_name = self.validate_camera_name(camera_name)

        scanning_device_name = None
        if "scanning_device_name" in kwargs:
            scanning_device_name = kwargs["scanning_device_name"]
        scanning_device_name = self.validate_scanning_device_name(scanning_device_name)

        scan_path_name = None
        if "scan_path_name" in kwargs:
            scan_path_name = kwargs["scan_path_name"]
        scan_path_name = self.validate_scan_path_name(scan_path_name)
                        
        scan = self.__factory.create("Scan",
                                     {"id": new_id(),
                                      "date": current_date().isoformat(),
                                      "person_names": [],
                                      "camera_name": camera_name,
                                      "scanning_device_name": scanning_device_name,
                                      "observation_unit_id": "",
                                      "scan_path_name": scan_path_name,
                                      "factor_values": {},
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


        
class Farm(IFarm):
    def __init__(self):
        self.__id = ""
        self.__short_name = ""
        self.__description = ""
        self.__license = ""
        self.__people = []
        self.__cameras = []
        self.__scanning_devices = []
        self.__zones = []

    def clone(self):
        c = copy.copy(self)
        c.__id = new_id()
        c.__people = []
        c.__scanning_devices = [s.clone for s in self.scanning_devices]
        c.__scan_paths = [s.clone for s in self.scan_paths]
        c.__zones = []
        return c
        
    @property
    def id(self):
        return self.__id
        
    @id.setter
    def id(self, value: str):
        self.__id = value

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
    def license(self) -> str:
        return self.__license

    @license.setter
    def license(self, value: str):
        self.__license = value
    
    @property
    def people(self) -> List[IPerson]:
        return self.__people
    
    @people.setter
    def people(self, value: List[IPerson]):
        self.__people = value

    def add_person(self, person: IPerson):
        if not person:
            raise Error() 
        self.people.append(person)

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
    def zones(self) -> List[IZone]:
        return self.__zones

    @zones.setter
    def zones(self, value: List[IZone]):
        self.__zones = value
        
    def add_zone(self, zone: IZone):
        zone.parent = self
        self.zones.append(zone)

    def parse(self, factory: IFactory, properties: dict):
        self.id = properties["id"]
        self.short_name = properties["short_name"]
        self.name = properties["name"]
        self.description = properties["description"]
        self.license = properties["license"]
        self.people = factory.create_list("Person", properties["people"])
        self.cameras = factory.create_list("Camera", properties["cameras"])
        self.scanning_devices = factory.create_list("ScanningDevice",
                                                    properties["scanning_devices"])
        self.zones = factory.create_list("Zone", properties["zones"])
        for zone in self.zones:
            zone.parent = self
        
    def serialize(self) -> dict:
        return { 'id': self.id,
                 'short_name': self.short_name,
                 'name': self.name,
                 'description': self.description,
                 'license': self.license,
                 'people': self.people,
                 'zones': self.zones,
                 'cameras': self.cameras,
                 'scanning_devices': self.scanning_devices }


class DefaultFactory(IFactory):
    def __init__(self):
        pass
    
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
            "ScanPath": ScanPath
        }
        constructor = switcher.get(classname)
        obj = constructor()
        obj.parse(self, properties)
        return obj
    
    def create_list(self, classname: str, properties: List[dict]) -> List[Any]:
        array = []
        for p in properties:
            obj = self.create(classname, p)
            array.append(obj)
        return array
