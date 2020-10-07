#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, make_response, abort
from flask import request, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api

import dateutil.parser

from romidata2.datamodel import *
from romidata2.webcache import WebCache

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class RomiResource(Resource):
    def __init__(self, app):
        self.__app = app

    @property
    def cache(self) -> WebCache:
        return self.__app.cache

    @property
    def db(self) -> IDatabase:
        return self.__app.database

    
class FarmList(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self):
        response = []
        for farm in self.db.select("Farm"):
            response.append({
                'id': farm.id,
                'short_name': farm.short_name,
                'name': farm.name,
                'location': farm.location,
                'photo': farm.photo.id if farm.photo else "" })
        return response

def cropImage(db, crop):
    # By default, use the farm's photo
    farm = crop.context
    image = farm.photo.id if farm.photo else ""
    
    mostRecentData = None
    
    for scan in crop.scans:
        for analysis in scan.analyses:
            if (analysis.short_name == "stitching"
                and analysis.state == IAnalysis.STATE_FINISHED):
                if (not mostRecentData or scan.date > mostRecentData):
                    results = db.file_read_json(analysis.results_file)
                    if 'cropped_map' in results: 
                        image = results['cropped_map']
                        mostRecentData = scan.date
    return image
            
    
class FarmInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, farm_id: str):
        farm = self.db.get_farm(farm_id)
        return {
            'id': farm.id,
            'short_name': farm.short_name,
            'name': farm.name,
            'description': farm.description,
            'address': farm.address,
            'country': farm.country,
            'location': farm.location,
            'photo': farm.photo.id if farm.photo else "",
            'license': farm.license,
            'people': [ p.serialize() for p in farm.people ],
            'crops': [{"id": obj.id,
                       "short_name": obj.short_name,
                       "photo": cropImage(self.db, obj)}
                      for obj in farm.observation_units
                      if obj.type == "crop" ] }#,
            #'zones': [{"id": obj.id, "short_name": obj.short_name} for obj in farm.zones ] }

    
class ZoneInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, zone_id: str):
        zone = self.db.lookup(zone_id)
        if zone.classname != "Zone":
            abort(404)
        farm = zone.farm
        return {
            'id': zone.id,
            'farm': farm.id,
            'short_name': zone.short_name
        }

    
class ObservationUnitInfo(RomiResource):
    def __init__(self, app, otype):
        super().__init__(app)
        self.__type = otype
        
    def get(self, obj_id: str):
        obj = self.db.lookup(obj_id)
        if (obj.classname != "ObservationUnit"
            or obj.type != self.__type):
            abort(404)
        farm = obj.context
        r = {
            'id': obj.id,
            'short_name': obj.short_name,
            'farm': farm.id,
            'zone': obj.zone.id,
            'parent': obj.parent.id if obj.parent else "",
            'children': [{
                "id": child.id,
                "type": child.type
            } for child in obj.children],
            'scans': [{
                "id": obj.id,
                "date": obj.date.isoformat()
            } for obj in obj.scans],
            'datastreams': [{
                "id": d.id,
                "observable": d.observable.name,
                "unit": d.unit.name
            } for d in obj.datastreams],
            'notes': [{
                "id": obj.id,
                "author": {"id": obj.author.id, "short_name": obj.author.short_name},
                "date": obj.date.isoformat(),
                "type": obj.type,
                "text": obj.text
            } for obj in obj.notes],
            'analyses': [{
                "id": analysis.id,
                "short_name": analysis.short_name,
                "name": analysis.name,
                "scan": analysis.scan.id if analysis.scan != None else "",
                "state": analysis.state
            } for analysis in obj.analyses]
        }
        return r


class CropInfo(ObservationUnitInfo):
    def __init__(self, app):
        super().__init__(app, 'crop')


class PlantInfo(ObservationUnitInfo):
    def __init__(self, app):
        super().__init__(app, 'plant')

        
class ScanInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, scan_id: str):
        scan = self.db.lookup(scan_id)
        if scan.classname != "Scan":
            abort(404)
        
        observation_unit = scan.observation_unit
        farm = observation_unit.context
        
        analyses = [{
            "id": analysis.id,
            "short_name": analysis.short_name,
            "name": analysis.name,
            "state": analysis.state
        } for analysis in scan.analyses]

        return {
            "id": scan.id,
            "farm": farm.id,
            "observation_unit": {'id': observation_unit.id, 'type': observation_unit.type },
            "date": scan.date.isoformat(),
            "images": [i.id for i in scan.images],
            "analyses": analyses
        }

    
class AnalysisInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, analysis_id: str):
        analysis = self.db.lookup(analysis_id)
        if analysis.classname != "Analysis":
            abort(404)
            
        observation_unit = analysis.observation_unit
        farm = observation_unit.context
            
        results = self.db.file_read_json(analysis.results_file)
        return {
            "id": analysis.id,
            "farm": farm.id,
            "observation_unit": {'id': observation_unit.id, 'type': observation_unit.type },
            "scan": analysis.scan.id if analysis.scan != None else "",
            "short_name": analysis.short_name,
            "name": analysis.name,
            "description": analysis.description,
            "state": analysis.state,
            "results": results
        }

    
class DataStreamInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, datastream_id: str):
        datastream = self.db.lookup(datastream_id)
        if datastream.classname != "DataStream":
            abort(404)
            
        observation_unit = datastream.observation_unit
        farm = observation_unit.context
            
        return {
            "id": datastream.id,
            "farm": farm.id,
            "observation_unit": {'id': observation_unit.id, 'type': observation_unit.type },
            "observable": datastream.observable.serialize(),
            "unit": datastream.unit.serialize()
        }


class NoteInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, ID: str):
        note = self.db.lookup(ID)
        if note.classname != "Note":
            abort(404)
            
        observation_unit = note.observation_unit
        farm = observation_unit.context
            
        return {
            "id": note.id,
            "farm": farm.id,
            "observation_unit": {'id': observation_unit.id, 'type': observation_unit.type },
            "author": { "id": note.author.id, "short_name": note.author.short_name},
            "date": note.date.isoformat(),
            "type": note.type,
            "text": note.text
        }

    
class DataStreamValues(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, datastream_id: str):
        datastream = self.db.lookup(datastream_id)
        if datastream.classname != "DataStream":
            abort(404)
            
        start = request.args.get('start', default=None, type=str)
        end = request.args.get('end', default=None, type=str)

        if start:
            start_date = dateutil.parser.parse(start)
        else:
            start_date = None

        if end:
            end_date = dateutil.parser.parse(end)
        else:
            end_date = None
            
        return datastream.select(self.db, start_date, end_date)

    
class RomiImage(RomiResource):
    """Class representing a image HTTP request, subclass of
    flask_restful's Resource class.
    """
    def __init__(self, app):
        super().__init__(app)
    
    def get(self, image_id):
        """Return the HTTP response with the image data. Resize the image if
        necessary.
        """
        size = request.args.get('size', default='thumb', type=str)
        if not size in ['orig', 'thumb', 'large']:
            size = 'thumb'
        orientation = request.args.get('orientation', default='default', type=str)
        if not orientation in ['orig', 'horizontal', 'vertical']:
            orientation = 'orig'
        direction = request.args.get('direction', default='cw', type=str)
        data, mimetype = self.cache.image_data(image_id, size, orientation, direction)
        response = make_response(data)
        response.headers['Content-Type'] = mimetype
        return response


class FarmWebApp(Flask):
    def __init__(self, db: IDatabase, cache: WebCache):
        super(FarmWebApp, self).__init__("Farmer's Dashboard API")
        self.__db = db
        self.__cache = cache
        CORS(self)
        self.__define_api()

    @property
    def database(self) -> IDatabase:
        return self.__db

    @property
    def cache(self) -> WebCache:
        return self.__cache
        
    def __define_api(self) -> None:
        self.__api = Api(self)
        print(self.__api.app)
        self.__api.add_resource(FarmList,
                                '/farms',
                                resource_class_kwargs={'app': self})
        
        self.__api.add_resource(FarmInfo,
                                '/farms/<string:farm_id>',
                                resource_class_kwargs={'app': self})
        
        self.__api.add_resource(ZoneInfo,
                                '/zones-xxx/<string:zone_id>',
                                resource_class_kwargs={'app': self})
                
        self.__api.add_resource(CropInfo,
                                '/crops/<string:obj_id>',
                                resource_class_kwargs={'app': self})
                
        self.__api.add_resource(PlantInfo,
                                '/plants/<string:obj_id>',
                                resource_class_kwargs={'app': self})
                
        self.__api.add_resource(ScanInfo,
                                '/scans/<string:scan_id>',
                                resource_class_kwargs={'app': self})
        
        self.__api.add_resource(AnalysisInfo,
                                '/analyses/<string:analysis_id>',
                                resource_class_kwargs={'app': self})

        self.__api.add_resource(DataStreamInfo,
                                '/datastreams/<string:datastream_id>',
                                resource_class_kwargs={'app': self})

        self.__api.add_resource(NoteInfo,
                                '/notes/<string:ID>',
                                resource_class_kwargs={'app': self})
        
        self.__api.add_resource(DataStreamValues,
                                '/datastreams/<string:datastream_id>/values',
                                resource_class_kwargs={'app': self})

        self.__api.add_resource(RomiImage,
                                '/images/<string:image_id>',
                                resource_class_kwargs={'app': self})
                
