#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, make_response
from flask import request, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api

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
        for farm in self.db.all:
            response.append({
                'id': farm.id,
                'short_name': farm.short_name,
                'name': farm.name })
        return response

    
class FarmInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, farm_id: str):
        farm = self.db.get(farm_id)
        return {
            'id': farm.id,
            'short_name': farm.short_name,
            'name': farm.name,
            'description': farm.description,
            'license': farm.license,
            'people': [ p.serialize() for p in farm.people ],
            'zones': [{"id": z.id, "short_name": z.short_name} for z in farm.zones ] }

    
class ZoneInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, farm_id: str, zone_id: str):
        farm = self.db.get(farm_id)
        zone = farm.get_zone(zone_id)
        return {
            'id': zone.id,
            'farm': farm.id,
            'short_name': zone.short_name,
            'scans': [{"id": s.id, "date": s.date.isoformat() } for s in zone.scans ] }

    
class ScanInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, farm_id: str, zone_id: str, scan_id: str):
        farm = self.db.get(farm_id)
        zone = farm.get_zone(zone_id)
        scan = zone.get_scan(scan_id)
        analysis_ids = [a.id for a in zone.analyses if a.scan_id == scan_id]
        analyses = []
        for analysis in zone.analyses:
            if analysis.scan_id == scan_id:
                analyses.append({
                    "id": analysis.id,
                    "short_name": analysis.short_name,
                    "name": analysis.name,
                    "state": analysis.state })            
        return {
            "id": scan.id,
            "farm": farm.id,
            "zone": zone.id,
            "date": scan.date.isoformat(),
            "images": [i.id for i in scan.images],
            "analyses": analyses
        }

    
class AnalysisInfo(RomiResource):
    def __init__(self, app):
        super().__init__(app)

    def get(self, farm_id: str, zone_id: str, analysis_id: str):
        farm = self.db.get(farm_id)
        zone = farm.get_zone(zone_id)
        analysis = zone.get_analysis(analysis_id)
        results = self.db.file_read_json(analysis.results_file)
        return {
            "id": analysis.id,
            "short_name": analysis.short_name,
            "name": analysis.name,
            "description": analysis.description,
            "state": analysis.state,
            "results": results
        }

    
class ZoneImage(RomiResource):
    """Class representing a image HTTP request, subclass of
    flask_restful's Resource class.
    """
    def __init__(self, app):
        super().__init__(app)
    
    def get(self, farm_id, zone_id, image_id):
        """Return the HTTP response with the image data. Resize the image if
        necessary.
        """
        size = request.args.get('size', default='thumb', type=str)
        if not size in ['orig', 'thumb', 'large']:
            size = 'thumb'
        data, mimetype = self.cache.image_data(farm_id, zone_id, image_id, size)
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
                                '/farms/<string:farm_id>/zones/<string:zone_id>',
                                resource_class_kwargs={'app': self})
                
        self.__api.add_resource(ScanInfo,
                                '/farms/<string:farm_id>/zones/<string:zone_id>/scans/<string:scan_id>',
                                resource_class_kwargs={'app': self})
        
        self.__api.add_resource(AnalysisInfo,
                                '/farms/<string:farm_id>/zones/<string:zone_id>/analyses/<string:analysis_id>',
                                resource_class_kwargs={'app': self})

        self.__api.add_resource(ZoneImage,
                                '/images/<string:farm_id>/<string:zone_id>/<string:image_id>',
                                resource_class_kwargs={'app': self})
                
        
 #        self.__api.add_resource(Image, '/farms/<string:farm_id>/zones/<string:zone_id>/files/<string:file_id>')
 #       self.__api.add_resource(Image, '/image/<string:farm_id>/<string:zone_id>/<string:file_id>')
