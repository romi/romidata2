#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Any
from os.path import join
import json

from romidata2.datamodel import *
from romidata2.impl import *
from romidata2.io import JsonImporter

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class Prototypes(IPrototypes):
    def __init__(self, basedir: str, factory: IFactory = None):
        self.__basedir = basedir
        if factory == None:
            self.__factory = DefaultFactory(None)
        else:
            self.__factory = factory
        self.__people = []
        self.__investigations = []
        self.__analyses = []
        self.__cameras = []
        self.__scanning_devices = []
        self.__biological_materials = []
        self.__studies = []
        self.__experimental_factors = []
        self.__observation_units = []
        self.__samples = []
        self.__scan_paths = []
        self.__load()
        
        
    @property
    def people(self) -> List[IPerson]:
        return self.__people

    @people.setter
    def people(self, value: List[IPerson]):
        self.__people = value

    @property
    def investigations(self) -> List[IInvestigation]:
        return self.__investigations

    @investigations.setter
    def investigations(self, value: List[IInvestigation]):
        self.__investigations = value

    @property
    def analyses(self) -> List[IAnalysis]:
        return self.__analyses

    @analyses.setter
    def analyses(self, value: List[IAnalysis]):
        self.__analyses = value

    @property
    def cameras(self) -> List[ICamera]:
        return self.__cameras

    @cameras.setter
    def cameras(self, value: List[ICamera]):
        self.__cameras = value

    @property
    def scanning_devices(self) -> List[IScanningDevice]:
        return self.__scanning_devices

    @scanning_devices.setter
    def scanning_devices(self, value: List[IScanningDevice]):
        self.__scanning_devices = value

    @property
    def biological_materials(self) -> List[IBiologicalMaterial]:
        return self.__biological_materials

    @biological_materials.setter
    def biological_materials(self, value: List[IBiologicalMaterial]):
        self.__biological_materials = value

    @property
    def studies(self) -> List[IStudy]:
        return self.__studies

    @studies.setter
    def studies(self, value: List[IStudy]):
        self.__studies = value

    @property
    def samples(self) -> List[ISample]:
        return self.__samples

    @samples.setter
    def samples(self, value: List[ISample]):
        self.__samples = value

    @property
    def observation_units(self) -> List[IObservationUnit]:
        return self.__observation_units

    @observation_units.setter
    def observation_units(self, values: List[IObservationUnit]):
        self.__observation_units = values

    def __load_prototypes(self, name: str) -> None:
        classNames = {
            "people": "Person",
            "investigations": "Investigation",
            "analyses": "Analysis",
            "cameras": "Camera",
            "scanning_devices": "ScanningDevice",
            "biological_materials": "BiologicalMaterial",
            "studies": "Study",
            "experimental_factors": "ExperimentalFactor",
            "samples": "Sample",
            "observation_units": "ObservationUnit",
            "scan_paths": "ScanPath"
        } 
        print("Loading '%s' prototypes:" % name)
        directory = join(self.__basedir, name)
        importer = JsonImporter(self.__factory)
        prototypes = importer.load_dir(directory, classNames[name])
        setattr(self, name, prototypes)

    def __load(self):
        self.__load_prototypes("people")
        self.__load_prototypes("investigations")
        self.__load_prototypes("analyses")
        self.__load_prototypes("cameras")
        self.__load_prototypes("scanning_devices")
        self.__load_prototypes("biological_materials")
        self.__load_prototypes("studies")
        self.__load_prototypes("experimental_factors")
        self.__load_prototypes("samples")
        self.__load_prototypes("observation_units")
        self.__load_prototypes("scan_paths")

    def __get(self, value: str, array: List[Any], key: str):
        r = None
        for v in array:
            if getattr(v, key) == value:
                r = v.clone()
                break
        return r
    
    def get_person(self, short_name: str):
        return self.__get(short_name, self.people, "short_name")
    
    def get_investigation(self, id: str):
        return self.__get(id, self.investigations, "id")
        
    def get_analysis(self, short_name: str):
        return self.__get(short_name, self.analyses, "short_name")
        
    def get_camera(self, short_name: str):
        return self.__get(short_name, self.cameras, "short_name")
        
    def get_scanning_device(self, short_name: str):
        return self.__get(short_name, self.scanning_devices, "short_name")
    
    def get_biological_material(self, short_name: str):
        return self.__get(short_name, self.biological_materials, "short_name")
    
    def get_study(self, id: str):
        return self.__get(id, self.studies, "id")
    
    def get_experimental_factor(self, factor_type: str):
        return self.__get(factor_type, self.experimental_factors, "short_name")
    
    def get_observation_unit(self, id: str):
        return self.__get(id, self.observation_units, "id")
    
    def get_scan_path(self, short_name: str):
        return self.__get(short_name, self.scan_paths, "short_name")
    
