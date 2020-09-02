import sys
from os.path import abspath

from PIL import Image

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.io import JsonExporter
from romidata2.db import FarmDatabase
from romidata2.impl import DefaultFactory, new_id

proto = Prototypes("prototypes")
db = FarmDatabase("db")
factory = DefaultFactory(db)
#db = Database("zip://farms.zip") # TODO: Fails...

def create_chatelain_farm(db):

    julie = factory.create("Person", {
        "short_name": "julie",
        "name": "Julie",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    julie.store()
    
    guillaume = factory.create("Person", {
        "short_name": "guillaume",
        "name": "Guillaume",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    guillaume.store()
    
    patrick = factory.create("Person", {
        "short_name": "patrick",
        "name": "Patrick",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    patrick.store()
    
    farm = factory.create("Farm", {
        "short_name": "chatelain",
        "name": "Chatelain Maraîchage",
        "description": "Historiquement présente depuis 250 ans au Thillay (95) en tant qu'agriculteur et pépiniériste, la famille Chatelain a lancé depuis 2017 une nouvelle activité autour du maraîchage. \n\nDans une volonté de produire sainement et localement, 5 hectares autour du Thillay ont été aménagés pour produire une diversité de fruits et légumes en pleine terre, hors sol ou sous tunnel. La production est certifiée Agriculture Biologique depuis Mai 2019 pour la parcelle au Thillay. Les autres parcelles sont cultivées selon des pratiques agricoles AB et seront toutes converties fin 2021. ",
        "address": "50 Route de Roissy, 95500 Le Thillay, France",
        "country": "FR",
        "photo": "",
        "location": [49.010521, 2.486378],
        "license": "CC BY-SA 4.0" })

    farm.add_person(julie)
    farm.add_person(guillaume)
    farm.add_person(patrick)

    relpath = db.farm_filepath(farm, "photo", "jpg")
    photo_file = db.new_file(farm.id, "farm", farm.id, "photo", relpath, "image/jpg")
    with open("chatelain.jpg", "rb") as f:
        data = f.read() 
        db.file_store_bytes(photo_file, data)
    farm.photo = photo_file
    
    picamera = proto.get_camera("picamera_v2")
    picamera.owner = farm
    db.store(picamera)
    farm.add_camera(picamera)
    
    camera_rail = proto.get_scanning_device("camera_rail")
    camera_rail.owner = farm
    db.store(camera_rail)
    farm.add_scanning_device(camera_rail)
    
    testzone = factory.create("Zone", {
        'farm': farm.id,
        'short_name': "testzone_rails"
    })
    testzone.store()
    farm.add_zone(testzone)
    
    testzone_observation = factory.create("ObservationUnit", {
        'type': 'crop',
        'short_name': "lettuce",
        'context': farm.id,
        'zone': testzone.id
    })
    testzone_observation.store()

    note = factory.create("Note", {
        'type': 'note',
        'observation_unit': "",
        'author': "",
        'date': "2019-04-15T12:00:00+02:00",
        'text': 'Lettuce planted out'
    })
    note.author = julie # FIXME
    note.observation_unit = testzone_observation # FIXME
    note.store()
    testzone_observation.add_note(note)
    
    note = factory.create("Note", {
        'type': 'note',
        'observation_unit': "",
        'author': "",
        'date': "2019-04-16T12:00:00+02:00",
        'text': 'First scan completed'
    })
    note.author = guillaume # FIXME
    note.observation_unit = testzone_observation # FIXME
    note.store()
    testzone_observation.add_note(note)
    
    farm.add_observation_unit(testzone_observation)
    testzone.add_observation_unit(testzone_observation)
    farm.store()
    

def create_valdaura_farm(db):
    
    jonathan = factory.create("Person", {
        "short_name": "jonathan",
        "name": "Jonathan",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    jonathan.store()
    
    farm = factory.create("Farm", {
        "short_name": "valdaura",
        "name": "Valdaura Self-Sufficient Labs - Iaac Barcelona",
        "description": "Valldaura Self-sufficient Labs is a project promoted by the Institute for Advanced Architecture of Catalonia for the creation of a self-sufficient habitat research centre. Located in the Collserola Natural Park, in the heart of the metropolitan area of Barcelona, it has laboratories for the production of energy, food and things, and develops projects and academic programmes in association with leading research centres around the world.",
        "address": "Ctra. BV-1415 (Horta-Cerdanyola), km 7, 08290, Barcelona, Spain",
        "country": "ES",
        "photo": "",
        "location": [41.450313, 2.133527],
        "license": "CC BY-SA 4.0" })

    farm.add_person(jonathan)

    relpath = db.farm_filepath(farm, "photo", "jpg")
    photo_file = db.new_file(farm.id, "farm", farm.id, "photo", relpath, "image/jpg")
    with open("valdaura.jpg", "rb") as f:
        data = f.read() 
        db.file_store_bytes(photo_file, data)
    farm.photo = photo_file
    
    farm.store()
    

if __name__ == "__main__":
    create_chatelain_farm(db)
    create_valdaura_farm(db)

    
