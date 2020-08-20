#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""romidata2.datamodel
==================

Provides the interfaces of the data, database, and factory objects in
this package.

"""
from abc import ABC, abstractmethod
from typing import List, Any
import copy
import functools
from datetime import datetime

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class IFactory(ABC):
    """IFactory is the interface for the object factory used in romidata.

    The objective of the factory is to hide the details of how the
    data objects are constructed. This allows to provide alternative
    implementations of these objects, for example, mock-ups for unit
    testing.

    """
    
    @abstractmethod
    def create(self, classname: str, properties: dict) -> Any:
        """Create a new object of the given type, using the properties passed as
        a dictionary.
        
        The recognized class names are: File, Person, Camera,
        ScanningDevice, BiologicalMaterial, Pose, Scan,
        SoftwareModule, Parameters, Task, ObservedVariable, Analysis,
        Study, Investigation, Zone, Farm, ExperimentalFactor,
        ObservationUnit, Sample, and ScanPath.

        """
        pass

    @abstractmethod
    def create_list(self, classname: str, properties: List[dict]) -> List[Any]:
        """Create a list of objects of the given type, using the list of
        properties passed as an agrument. This function calls create()
        on each of the dictionaries in the list and returns the reults
        as a list.
        """ 
        pass
    

class IPrototypes(ABC):
    """IPrototypes is the interface for the database of prototypes. A
    prototype as an object that serves to create another object by
    cloning. It is used to facilitate the creation of data objects by
    cloning an existing description with pre-filled data fields.

    The prototypes database loads the list of person, analysis,
    ... prototypes. The get_xxx() methods return a clone of the
    objects in the database that can be modified and stored according
    to your needs.

    """
    @abstractmethod
    def get_person(self, short_name: str):
        """Get a prototype of the person object with the given short name."""
        pass
    
    @abstractmethod
    def get_investigation(self, id: str):
        """Get a prototype of the investigation with the given id."""
        pass
        
    @abstractmethod
    def get_analysis(self, short_name: str):
        """Get a prototype of the analysis with the given short name."""
        pass
        
    @abstractmethod
    def get_camera(self, short_name: str):
        """Get a prototype of the camera with the given short name."""
        pass
        
    @abstractmethod
    def get_scanning_device(self, short_name: str):
        """Get a prototype of the scanning device with the given short name."""
        pass
    
    @abstractmethod
    def get_biological_material(self, short_name: str):
        """Get a prototype of the biological material object with the given
        short name.
        """
        pass
    
    @abstractmethod
    def get_study(self, id: str):
        """Get a prototype of the study with the given id."""
        pass


class BaseClass(ABC):
    """This is the base class for all data objects. It defines the clone,
    serialize, and parse methods that have to be implemented by all
    subclasses.

    """

    @abstractmethod
    def clone(self):
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass

    @property
    @abstractmethod
    def classname(self) -> str:
        pass

    @abstractmethod
    def serialize(self, recursive=False) -> dict:
        pass

    def store_default(self, db: Any) -> None:
        db.store_object(self.id, self.classname, self)

    def store_list(self, db: Any, array, recursive=False) -> None:
        for obj in array:
            obj.store(db, recursive)

    def store_id_list(self, db: Any, array, recursive=False) -> None:
        for the_id in array:
            obj = db.lookup(the_id)
            if obj:
                obj.store(db, recursive)
            else:
                raise ValueError("ID with value %s does not exist" % the_id)

    @abstractmethod
    def store(self, db: Any, recursive=False) -> None:
        pass

    def restore(self, db: Any) -> None:
        pass

    def lookup_id_list(self, db: Any, array: List[str]) -> List[Any]:
        r = []
        for the_id in array:
            obj = db.lookup(the_id)
            if obj:
                r.append(obj)
            else:
                raise ValueError("ID with value %s does not exist" % the_id)
        return r
    
    @abstractmethod
    def parse(self, factory: IFactory, properties: dict) -> dict:
        pass
        
    def find(self, given_value: str, array: List[Any], attr: str):
        r = None
        for obj in array:
            obj_value = getattr(obj, attr)
            if obj_value == given_value:
                r = obj
                break
        return r


        
class IFile(BaseClass):

    @property
    def classname(self):
        return "File"

    @property
    @abstractmethod
    def source_name(self) -> List[str]:
        pass

    @source_name.setter
    @abstractmethod
    def source_name(self, value: str):
        pass

    @property
    @abstractmethod
    def source_id(self) -> List[str]:
        pass

    @source_id.setter
    @abstractmethod
    def source_id(self, value: str):
        pass

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def date_created(self) -> datetime:
        pass

    @date_created.setter
    @abstractmethod
    def date_created(self, value: datetime):
        pass
        
    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @path.setter
    @abstractmethod
    def path(self, value: str):
        pass

    @property
    @abstractmethod
    def mimetype(self) -> str:
        pass

    @mimetype.setter
    @abstractmethod
    def mimetype(self, value: str):
        pass



class IPerson(BaseClass):

    @property
    def classname(self):
        return "Person"

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @email.setter
    @abstractmethod
    def email(self, value: str):
        pass

    @property
    @abstractmethod
    def affiliation(self) -> str:
        pass

    @affiliation.setter
    @abstractmethod
    def affiliation(self, value: str):
        pass
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass

    @property
    @abstractmethod
    def role(self) -> str:
        pass

    @role.setter
    @abstractmethod
    def role(self, value: str):
        pass

    
class IParameters(BaseClass):

    @property
    def classname(self):
        return "Parameters"
    
    @abstractmethod
    def get_value(self, key: str) -> Any:
        return self.__values[key]

    @abstractmethod
    def set_value(self, key: str, value: Any):
        pass

    @property
    @abstractmethod
    def values(self) -> dict:
        pass


class ISoftwareModule(BaseClass):

    @property
    def classname(self):
        return "SoftwareModule"

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @version.setter
    @abstractmethod
    def version(self, value: str):
        pass

    @property
    @abstractmethod
    def repository(self) -> str:
        pass

    @repository.setter
    @abstractmethod
    def repository(self, value: str):
        pass

    @property
    @abstractmethod
    def branch(self) -> str:
        pass

    @branch.setter
    @abstractmethod
    def branch(self, value: str):
        pass
    

class ICamera(BaseClass):

    @property
    def classname(self):
        return "Camera"
        
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass
        
    @property
    @abstractmethod
    def lens(self) -> str:
        pass

    @lens.setter
    @abstractmethod
    def lens(self, value: str):
        pass
    
    @property
    @abstractmethod
    def software_module(self) -> ISoftwareModule:
        pass

    @software_module.setter
    @abstractmethod
    def software_module(self, value: ISoftwareModule):
        pass

    @property
    @abstractmethod
    def parameters(self) -> IParameters:
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, values: IParameters):
        pass

    
class IScanningDevice(BaseClass):

    @property
    def classname(self):
        return "ScanningDevice"
    
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass
    
    @property
    @abstractmethod
    def software_module(self) -> ISoftwareModule:
        pass

    @software_module.setter
    @abstractmethod
    def software_module(self, value: ISoftwareModule):
        pass

    @property
    @abstractmethod
    def parameters(self) -> IParameters:
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, values: IParameters):
        pass

        
class IScanPath(BaseClass):

    @property
    def classname(self):
        return "ScanPath"
        
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @type.setter
    @abstractmethod
    def type(self, value: str):
        pass

    @property
    @abstractmethod
    def parameters(self) -> IParameters:
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, values: IParameters):
        pass

    
class ISample(BaseClass):

    @property
    def classname(self):
        return "Sample"
        
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass
        
    @property
    @abstractmethod
    def development_stage(self) -> str:
        pass

    @development_stage.setter
    @abstractmethod
    def development_stage(self, value: str):
        pass

    @property
    @abstractmethod
    def anatomical_entity(self) -> str:
        pass

    @anatomical_entity.setter
    @abstractmethod
    def anatomical_entity(self, value: str):
        pass


class IObservationUnit(BaseClass):

    @property
    def classname(self):
        return "ObservationUnit"
        
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @type.setter
    @abstractmethod
    def type(self, value: str):
        pass
    
    @property
    @abstractmethod
    def spatial_distribution(self) -> str:
        pass

    @spatial_distribution.setter
    @abstractmethod
    def spatial_distribution(self, value: str):
        pass

    @property
    @abstractmethod
    def factor_values(self) -> dict:
        pass

    @factor_values.setter
    @abstractmethod
    def factor_values(self, values: dict):
        pass

    def set_factor_value(self, key: str, value: str):
        self.factor_values[key] = value

    @property
    @abstractmethod
    def samples(self) -> List[ISample]:
        pass

    @samples.setter
    @abstractmethod
    def samples(self, values: List[ISample]):
        pass

    def add_sample(self, value: ISample):
        self.samples.append(value)
    
    @property
    @abstractmethod
    def description_file(self) -> str:
        pass

    @description_file.setter
    @abstractmethod
    def description_file(self, value: str):
        pass


class IBiologicalMaterial(BaseClass):

    @property
    def classname(self):
        return "BiologicalMaterial"

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def genus(self) -> str:
        pass

    @genus.setter
    @abstractmethod
    def genus(self, value: str):
        pass

    @property
    @abstractmethod
    def species(self) -> str:
        pass

    @species.setter
    @abstractmethod
    def species(self, value: str):
        pass

    @property
    @abstractmethod
    def intraspecific_name(self) -> str:
        pass

    @intraspecific_name.setter
    @abstractmethod
    def intraspecific_name(self, value: str):
        pass

    @property
    @abstractmethod
    def source_id(self) -> str:
        pass

    @source_id.setter
    @abstractmethod
    def source_id(self, value: str):
        pass

    @property
    @abstractmethod
    def source_doi(self) -> str:
        pass

    @source_doi.setter
    @abstractmethod
    def source_doi(self, value: str):
        pass

        
class IPose(BaseClass):

    @property
    def classname(self):
        return "Pose"


class IUnit():

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class IObservable():

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    
class IDataStream(BaseClass):

    @property
    def classname(self):
        return "DataStream"

    @property
    @abstractmethod
    def observable(self) -> IObservable:
        pass

    @property
    @abstractmethod
    def unit(self) -> IUnit:
        pass
    
    @abstractmethod
    def get_values(self, db) -> List[dict]:
        pass
    
    @abstractmethod
    def select(self, db, start_date: datetime = None,
               end_date: datetime = None) -> List[dict]:
        pass


class IBoundingBox(BaseClass):

    @property
    def classname(self):
        return "BoundingBox"

    @property
    def x(self) -> List[float]:
        pass
    
    @x.setter
    @abstractmethod
    def x(self, values: List[float]):
        pass
    
    @property
    def y(self) -> List[float]:
        pass
    
    @y.setter
    @abstractmethod
    def y(self, values: List[float]):
        pass
        
    @property
    def z(self) -> List[float]:
        pass
    
    @z.setter
    @abstractmethod
    def z(self, values: List[float]):
        pass
    
    
class IScan(BaseClass):

    @property
    def classname(self):
        return "Scan"
        
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def parent(self) -> Any:
        pass

    @parent.setter
    @abstractmethod
    def parent(self, value: Any):
        pass

    @property
    @abstractmethod
    def date(self) -> datetime:
        pass

    @date.setter
    @abstractmethod
    def date(self, value: datetime):
        pass

    @property
    @abstractmethod
    def person_names(self) -> List[str]:
        pass

    @person_names.setter
    @abstractmethod
    def person_names(self, values: List[str]):
        pass

    def add_person_name(self, value: str):
        self.get_person_names.append(value)

    @property
    @abstractmethod
    def camera_name(self) -> str:
        pass

    @camera_name.setter
    @abstractmethod
    def camera_name(self, value: str):
        pass

    @property
    @abstractmethod
    def scanning_device_name(self) -> str:
        pass

    @scanning_device_name.setter
    @abstractmethod
    def scanning_device_name(self, value: str):
        pass

    @property
    @abstractmethod
    def observation_unit_id(self) -> str:
        pass

    @observation_unit_id.setter
    @abstractmethod
    def observation_unit_id(self, value: str):
        pass

    @property
    @abstractmethod
    def bounding_box(self) -> IBoundingBox:
        pass

    @bounding_box.setter
    @abstractmethod
    def bounding_box(self, value: IBoundingBox):
        pass
    
    @abstractmethod
    def camera_pose_types(self) -> List[str]:
        pass

    @abstractmethod
    def camera_poses(self, pose_type: str):
        pass

    @abstractmethod
    def set_camera_pose(self, img_id: str, pose_type: str, pose: IPose):
        pass

    @abstractmethod
    def get_camera_pose(self, img_id: str, pose_type: str) -> IPose:
        pass
    
    @property
    @abstractmethod
    def factor_values(self) -> dict:
        pass

    @factor_values.setter
    @abstractmethod
    def factor_values(self, values: dict):
        pass

    @abstractmethod
    def set_factor_value(self, key: str, value: str):
        pass

    @property
    @abstractmethod
    def scan_path_name(self) -> str:
        pass

    @scan_path_name.setter
    @abstractmethod
    def scan_path_name(self, value: str):
        pass

    @property
    @abstractmethod
    def images(self) -> List[IFile]:
        pass

    
class ITask(BaseClass):
    STATE_DEFINED = "Defined"
    STATE_RUNNING = "Running"
    STATE_FINISHED = "Finished"
    STATE_ERROR = "Error"
    STATES = ["Defined", "Running", "Finished", "Error"]

    @property
    def classname(self):
        return "Task"
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
            
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def software_module(self) -> ISoftwareModule:
        pass

    @software_module.setter
    @abstractmethod
    def software_module(self, value: ISoftwareModule):
        pass

    @property
    @abstractmethod
    def parameters(self) -> IParameters:
        pass

    @parameters.setter
    @abstractmethod
    def parameters(self, value: IParameters):
        pass
        
    @property
    @abstractmethod
    def state(self) -> str:
        pass

    @state.setter
    @abstractmethod
    def state(self, value: str):
        pass

    @property
    @abstractmethod
    def input_files(self) -> List[str]:
        pass

    @abstractmethod
    def add_input_file(self, id: str):
        pass

    @property
    @abstractmethod
    def output_files(self) -> List[str]:
        pass

    @output_files.setter
    @abstractmethod
    def output_files(self, values: List[str]) -> None:
        pass

    @abstractmethod
    def add_output_file(self, output_file: IFile):
        pass
        
    @property
    @abstractmethod
    def log_file(self):
        pass

    @log_file.setter
    @abstractmethod
    def log_file(self, value: str):
        pass
    

class IObservedVariable(BaseClass):

    @property
    def classname(self):
        return "ObservedVariable"
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
        
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def trait(self) -> str:
        pass

    @trait.setter
    @abstractmethod
    def trait(self, value: str):
        pass
        
    @property
    @abstractmethod
    def scale(self) -> str:
        pass

    @scale.setter
    @abstractmethod
    def scale(self, value: str):
        pass
        
    @property
    @abstractmethod
    def time_scale(self) -> str:
        pass

    @time_scale.setter
    @abstractmethod
    def time_scale(self, value: str):
        pass


class IAnalysis(BaseClass):
    STATE_DEFINED = "Defined"
    STATE_RUNNING = "Running"
    STATE_FINISHED = "Finished"
    STATE_ERROR = "Error"

    @property
    def classname(self):
        return "Analysis"
            
    @property
    @abstractmethod
    def parent(self):
        pass
        
    @parent.setter
    @abstractmethod
    def parent(self, value: Any):
        pass
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass
    
    @property
    @abstractmethod
    def short_name(self):
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass
    
    @property
    @abstractmethod
    def scan_id(self) -> str:
        pass

    @scan_id.setter
    @abstractmethod
    def scan_id(self, value: str):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def state(self) -> str:
        pass

    @state.setter
    @abstractmethod
    def state(self, value: str):
        pass

    @property
    @abstractmethod
    def observed_variables(self) -> List[IObservedVariable]:
        pass

    @observed_variables.setter
    @abstractmethod
    def observed_variables(self, values: List[IObservedVariable]):
        pass

    @property
    @abstractmethod
    def tasks(self) -> List[ITask]:
        pass

    @tasks.setter
    @abstractmethod
    def tasks(self, values: List[ITask]) -> None:
        pass

    @abstractmethod
    def get_task(self, id_or_short_name: str) -> ITask:
        pass

    @property
    @abstractmethod
    def results_file(self) -> IFile:
        pass

    
class IExperimentalFactor(BaseClass):

    @property
    def classname(self):
        return "ExperimentalFactor"
    
    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass
        
    @property
    @abstractmethod
    def values(self) -> List[str]:
        pass

    @values.setter
    @abstractmethod
    def values(self, value: List[str]):
        pass


class StudyAndZoneBase(BaseClass):
        
    @property
    @abstractmethod
    def id(self):
        pass

    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass

#    @property
#    @abstractmethod
#    def parent(self) -> Any:
#        pass
#
#    @id.setter
#    @abstractmethod
#    def parent(self, value: Any):
#        pass

    @property
    @abstractmethod
    def files(self) -> List[IFile]:
        pass

    @files.setter
    @abstractmethod
    def files(self, values: List[IFile]):
        pass

    def add_file(self, f: IFile):
        if not f:
            raise ValueError("Expected a file object as argument")
        f.parent = self
        self.files.append(f)

    def get_file(self, file_id: str):
        return self.find(file_id, self.files, "id")
            
    def get_files_by_source(self, source_name: str, source_id: str, short_name: str):
        r = []
        for f in self.files:
            if ((not source_name or f.source_name == source_name)
                and (not source_id or f.source_id == source_id)
                and (not short_name or f.short_name == short_name)):
                r.append(f)
        return r
            
#    @property
#    @abstractmethod
#    def scans(self) -> List[IScan]:
#        pass
#
#    @scans.setter
#    @abstractmethod
#    def scans(self, values: List[IScan]):
#        pass
#
#    def add_scan(self, scan: IScan):
#        if not scan:
#            raise ValueError("Expected a scan object as argument")
#        scan.parent = self
#        self.scans.append(scan)
#
#    def get_scan(self, scan_id: str):
#        return self.find(scan_id, self.scans, "id")
            
#    @property
#    @abstractmethod
#    def analyses(self) -> List[IAnalysis]:
#        pass
#
#    @analyses.setter
#    @abstractmethod
#    def analyses(self, values: List[IAnalysis]):
#        pass
#
#    @abstractmethod
#    def add_analysis(self, value: IAnalysis):
#        pass
#
#    def get_analysis(self, analysis_id: str):
#        return self.find(analysis_id, self.analyses, "id")

    @property
    @abstractmethod
    def scan_paths(self) -> List[IScanPath]:
        pass

    @scan_paths.setter
    @abstractmethod
    def scan_paths(self, values: List[IScanPath]):
        pass

    def add_scan_path(self, value: IScanPath):
        if not value:
            raise ValueError("Expected an scan path as argument")
        self.scan_paths.append(value)

    @abstractmethod
    def new_scan(self, db, **kwargs):
        pass

    
class IStudy(StudyAndZoneBase):

    @property
    def classname(self):
        return "Study"

    @property
    @abstractmethod
    def investigation(self) -> Any:
        pass

    @investigation.setter
    @abstractmethod
    def investigation(self, value: Any):
        pass
    
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @title.setter
    @abstractmethod
    def title(self, value: str):
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def people(self) -> List[IPerson]:
        pass

    @people.setter
    @abstractmethod
    def people(self, values: List[IPerson]):
        pass
    
    def add_person(self, value: IPerson):
        if not value:
            raise ValueError("Expected a person as argument")
        self.people.append(value)
    
    @property
    @abstractmethod
    def cameras(self) -> List[ICamera]:
        pass

    @cameras.setter
    @abstractmethod
    def cameras(self, values: List[ICamera]):
        pass

    def add_camera(self, value: ICamera):
        if not value:
            raise ValueError("Expected a camera object as argument")
        self.cameras.append(value)

    @property
    @abstractmethod
    def scanning_devices(self) -> List[IScanningDevice]:
        pass

    @scanning_devices.setter
    @abstractmethod
    def scanning_devices(self, values: List[ICamera]):
        pass

    def add_scanning_device(self, value: IScanningDevice):
        if not value:
            raise ValueError("Expected a scanning device as argument")
        self.scanning_devices.append(value)

    @property
    @abstractmethod
    def experimental_factors(self) -> List[IExperimentalFactor]:
        pass

    @experimental_factors.setter
    @abstractmethod
    def experimental_factors(self, values: List[IExperimentalFactor]):
        pass

    def add_experimental_factor(self, value: IExperimentalFactor):
        if not value:
            raise ValueError("Expected an experimental factor as argument")
        self.experimental_factors.append(value)

    @property
    @abstractmethod
    def observation_units(self) -> List[IObservationUnit]:
        pass

    @observation_units.setter
    @abstractmethod
    def observation_units(self, values: List[IObservationUnit]):
        pass

    def add_observation_unit(self, value: IObservationUnit):
        if not value:
            raise ValueError("Expected an observation unit as argument")
        self.observation_units.append(value)

        
class IZone(StudyAndZoneBase):

    @property
    def classname(self):
        return "Zone"

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
    
    @property
    @abstractmethod
    def farm(self) -> str:
        pass
        
    @farm.setter
    @abstractmethod
    def farm(self, value: str):
        pass
    
    @property
    @abstractmethod
    def scans(self) -> List[IScan]:
        pass
    
    @property
    @abstractmethod
    def analyses(self, db) -> List[IAnalysis]:
        pass

    @abstractmethod
    def add_analysis(self, value: IAnalysis, db):
        pass
    
    @property
    @abstractmethod
    def datastreams(self) -> List[IDataStream]:
        pass

    @abstractmethod
    def add_datastream(self, value: IDataStream, db):
        pass


class IFarm(BaseClass):

    @property
    def classname(self):
        return "Farm"
        
    @property
    @abstractmethod
    def id(self):
        pass
    
    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def license(self) -> str:
        pass

    @license.setter
    @abstractmethod
    def license(self, value: str):
        pass
    
    @property
    @abstractmethod
    def people(self) -> List[IPerson]:
        pass

    @abstractmethod
    def add_person(self, person: IPerson, db):
        pass
    
    @property
    @abstractmethod
    def cameras(self) -> List[ICamera]:
        pass

    @cameras.setter
    @abstractmethod
    def cameras(self, values: List[ICamera]):
        pass

    def add_camera(self, value: ICamera):
        if not value:
            raise ValueError("Expected a camera object as argument")
        self.cameras.append(value)

    @property
    @abstractmethod
    def scanning_devices(self) -> List[IScanningDevice]:
        pass

    @scanning_devices.setter
    @abstractmethod
    def scanning_devices(self, values: List[ICamera]):
        pass

    def add_scanning_device(self, value: IScanningDevice):
        if not value:
            raise ValueError("Expected a scanning device as argument")
        self.scanning_devices.append(value)

    @property
    @abstractmethod
    def zones(self) -> List[IZone]:
        pass

    @abstractmethod
    def add_zone(self, zone: IZone, db):
        pass

    @abstractmethod
    def get_zone(self, id_or_name: str):
        pass

    
class IInvestigation(BaseClass):

    @property
    def classname(self):
        return "Investigation"
        
    @property
    @abstractmethod
    def id(self):
        pass
    
    @id.setter
    @abstractmethod
    def id(self, value: str):
        pass

    @property
    @abstractmethod
    def short_name(self) -> str:
        pass

    @short_name.setter
    @abstractmethod
    def short_name(self, value: str):
        pass
        
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @title.setter
    @abstractmethod
    def title(self, value: str):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str):
        pass

    @property
    @abstractmethod
    def license(self) -> str:
        pass

    @license.setter
    @abstractmethod
    def license(self, value: str):
        pass

    @property
    @abstractmethod
    def publications(self) -> List[str]:
        pass

    @abstractmethod
    def add_publication(self, ref: str):
        pass
    
    @property
    @abstractmethod
    def people(self) -> List[IPerson]:
        pass

    @people.setter
    @abstractmethod
    def people(self, values: List[IPerson]):
        pass

    def add_person(self, person: IPerson):
        self.people.append(person)

    @property
    @abstractmethod
    def studies(self) -> List[IStudy]:
        pass

    @studies.setter
    @abstractmethod
    def studies(self, values: List[IStudy]):
        pass

    def add_study(self, study: IStudy):
        self.studies.append(study)

    def get_study(self, id_or_short_name: str) -> IZone:
        return (self.find(id_or_short_name, self.studies, "id")
                or self.find(id_or_short_name, self.studies, "short_name"))

    def get(self, id_or_short_name) -> Any:
        return self.get_study(id_or_short_name)


    
class IDatabase(ABC):

    @abstractmethod
    def lookup(self, obj_id: str) -> BaseClass:
        pass
    
    @abstractmethod
    def select(self, classname: str, prop: str, value: str) -> List[BaseClass]:
        pass
        
    @abstractmethod
    def store_object(self, obj_id: str, classname: str, obj: Any) -> None:
        pass
    
    @abstractmethod
    def store(self, obj: Any, recursive=False) -> None:
        pass
    
    @abstractmethod
    def new_file(self, source_name: str, source_id: str,
                 short_name: str, relpath: str, mimetype: str) -> IFile:
        pass

    @abstractmethod
    def get_file(self, file_id: str) -> IFile:
        pass
        
    @abstractmethod
    def select_files(self, source_name: str,
                     source_id: str, short_name: str) -> List[IFile]:
        pass
        
    @abstractmethod
    def file_store_text(self, f: IFile, text: str) -> None:
        pass
    
    @abstractmethod
    def file_store_bytes(self, f: IFile, data: bytes) -> None:
        pass
    
    @abstractmethod
    def file_read_text(self, f: IFile) -> str:
        pass
    
    @abstractmethod
    def file_read_json(self, f: IFile) -> Any:
        pass
    
    @abstractmethod
    def file_read_bytes(self, f: IFile) -> bytes:
        pass
   
