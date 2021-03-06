#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""romidata2.webcache
==================

Provides utility functions that are used in combination with the
IDatabase interface to create downsized versions of images (and in the
future also of point clouds and mesh resources). The web cache can
either serve data from an Investigation database or a Farm database.
The resources are identified using either the investigation, the
study, and the file IDs when used with a Investigation database, or
using either the farm, the zone, and the file IDs when used with a
Farm database The downsized versions are cached in the directory
passed as argument.

The following size specifications are available:

* Images: 'thumb' (max. 150x150), 'large' (max. 1500x1500), and 'orig' (original size).

Examples
--------
>>> from romidata2.db import FarmDatabase
>>> from romidata2.webcache import WebCache
>>> db = FarmDatabase("demo/db")
>>> cache = WebCache(db, "farms", "/tmp/romicache")
>>> binary_image, mimetype = webcache.image_data('image000', 'thumb')

"""
import os
from io import BytesIO

import hashlib
from PIL import Image

from romidata2.datamodel import IDatabase

__author__ = "Peter Hanappe"
__copyright__ = "Copyright 2020, Sony Computer Science Laboratories"
__credits__ = ["Peter Hanappe"]
__license__ = "Affero General Public License"
__version__ = "3"
__maintainer__ = "Peter Hanappe"
__email__ = "peter@hanappe.com"
__status__ = "Prototype"
__version__ = "0.0.1"

class WebCache():
    """Class implementing a cache to store resources (images and other) in
    several resolutions to speed up the download for the web interface.


    Attributes
    ----------
    db : IDatabase
        The database object
    db_type : str
        One of "farms" or "investigations".
    path: str
        ``The path of the local cache directory.

    """
    def __init__(self, db: IDatabase, db_type: str, path: str):
        self.__db = db
        self.__db_type = db_type
        self.__path = path
        os.makedirs(self.__path, exist_ok=True)

    def __hash(self, components):
        """Computes a SHA1 hash.
    
        Parameters
        ----------
        components: List[str]
            The list of strings that define the resource. It should
            include the resource type ('image', ...), the file ID, 
            the size, and the additional features that uniquely defines
            the resource. 

        """
        m = hashlib.sha1()
        key = '|'.join(components)
        m.update(key.encode('utf-8'))
        return m.hexdigest()

    # Image
    def __image_hash(self, file_id, size, orientation, direction):
        """Compute a hash key for the image.
    
        Parameters
        ----------
        file_id: str
            The ID of the file in the fileset
        size: str
            The requested size ('orig', 'large', or 'thumb')
        orientation: str
            The requested orientation ('orig', 'horizontal', or 'vertical')
        direction: str
            The direction of the rotation ('cw', 'ccw')

        """
        return self.__hash(["image", file_id, size, orientation, direction])

    def __image_resize(self, img, max_size):
        """Resize an image to the cache.
    
        Parameters
        ----------
        img: PIL Image
            The image
        size: str
            The requested size ('orig', 'large', or 'thumb')

        """
        img.thumbnail((max_size, max_size))
        return img

    def __cache_image(self, file_id, size, orientation, direction):
        """Add an image to the cache.
    
        Parameters
        ----------
        file_id: str
            The ID of the file in the fileset
        size: str
            The requested size ('orig', 'large', or 'thumb')
        orientation: str
            The requested orientation ('orig', 'horizontal', or 'vertical')
        direction: str
            The direction of the rotation ('cw', 'ccw')

        """
        ifile = self.__db.get_file(file_id)
        image = self.__db.file_read_bytes(ifile)
        dst = os.path.join(self.__path, self.__image_hash(file_id, size, orientation, direction))
        
        resolutions = { "large": 1500, "thumb": 150 }
        maxsize = resolutions.get(size) 
        
        image = Image.open(BytesIO(image))
        image.load()
        w, h = image.size
        image_orientation = 'horizontal' if w > h else 'vertical'
            
        image = self.__image_resize(image, maxsize)

        if orientation != 'orig' and orientation != image_orientation:
            angle = -90 if direction == 'cw' else 90
            image = image.rotate(angle, expand=True)
            
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(dst, "JPEG", quality=84)
        
        print("Converted (%s) to %s, size %d" % (file_id, dst, maxsize))

        return dst


    def __cached_image_data(self, file_id, size, orientation, direction):
        """Return cached image data.
        
        Returns the data of a cached image. If the image is not yet
        cached, it will be added.
    
        Parameters
        ----------
        file_id: str
            The ID of the file in the fileset
        size: str
            The requested size ('orig', 'large', or 'thumb')
        orientation: str
            The requested orientation ('orig', 'horizontal', or 'vertical')
        direction: str
            The direction of the rotation ('cw', 'ccw')

        """
        data = None
        path = os.path.join(self.__path, self.__image_hash(file_id, size, orientation, direction))
        if not os.path.isfile(path):
            self.__cache_image(file_id, size, orientation, direction)
        with open(path, mode="rb") as f:
            data = f.read()
            f.close()
        return data

    
    def image_data(self, file_id, size, orientation, direction):
        """Return image data.
        
        Returns the data of a given image file in the database.
    
        Parameters
        ----------
        file_id: str
            The ID of the file in the fileset
        size: str
            The requested size ('orig', 'large', or 'thumb')
        orientation: str
            The requested orientation ('orig', 'horizontal', or 'vertical')
        direction: str
            The direction of the rotation ('cw', 'ccw')

        """
        if not size in ['orig', 'thumb', 'large']:
            raise ValueError("Invalid size: %s" % size)
        if not orientation in ['orig', 'horizontal', 'vertical']:
            raise ValueError("Invalid orientation: %s" % orientation)
        if not direction in ['cw', 'ccw']:
            raise ValueError("Invalid direction: %s" % direction)
        
        if size == "orig" and orientation == 'orig':
            print("Using original file")
            ifile = self.__db.get_file(file_id)
            return self.__db.file_read_bytes(ifile), ifile.mimetype
        else:
            print("Using cached file")
            return self.__cached_image_data(file_id, size, orientation, direction), "image/jpg"

