import sys
from os.path import abspath

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.io import JsonExporter
from romidata2.db import FarmDatabase
from romidata2.impl import DefaultFactory, new_id

factory = DefaultFactory()
proto = Prototypes("prototypes")
db = FarmDatabase("db")
#db = Database("zip://farms.zip") # TODO: Fails...

def create_chatelain_farm():
    julie = factory.create("Person", {
        "id": new_id(),
        "short_name": "julie",
        "name": "Julie",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    guillaume = factory.create("Person", {
        "id": new_id(),
        "short_name": "guillaume",
        "name": "Guillaume",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    patrick = factory.create("Person", {
        "id": new_id(),
        "short_name": "patrick",
        "name": "Patrick",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    farm = factory.create("Farm", {
        "id": new_id(),
        "short_name": "chatelain",
        "name": "Chatelain Maraîchage",
        "description": "Historiquement présente depuis 250 ans au Thillay (95) en tant qu'agriculteur et pépiniériste, la famille Chatelain a lancé depuis 2017 une nouvelle activité autour du maraîchage. \n\nDans une volonté de produire sainement et localement, 5 hectares autour du Thillay ont été aménagés pour produire une diversité de fruits et légumes en pleine terre, hors sol ou sous tunnel. La production est certifiée Agriculture Biologique depuis Mai 2019 pour la parcelle au Thillay. Les autres parcelles sont cultivées selon des pratiques agricoles AB et seront toutes converties fin 2021. ",
        "license": "CC BY-SA 4.0",
        "people": [ julie.serialize(),     # TODO: avoid serialize()
                    guillaume.serialize(),
                    patrick.serialize() ],
        "cameras": [],
        "scanning_devices": [],
        "zones": [] })
    
    realsense = proto.get_camera("realsense")
    farm.add_camera(realsense)
    
    dev_robot = proto.get_scanning_device("dev_robot")
    farm.add_scanning_device(dev_robot)
    
    testzone = factory.create("Zone", {
        'id': new_id(),
        'short_name': "testzone_rails",
        'scan_paths': [],
        'files': [],
        'scans': [],
        'analyses': [] })
    
    linear_4m = proto.get_scan_path("linear_4m")
    testzone.add_scan_path(linear_4m)
    
    farm.add_zone(testzone)
    db.store(farm)
    

def create_valdaura_farm():
    jonathan = factory.create("Person", {
        "id": new_id(),
        "short_name": "jonathan",
        "name": "Jonathan",
        "email": "",
        "affiliation": "",
        "role": ""        
    })
    testzone = factory.create("Zone", {
        'id': new_id(),
        'short_name': "testzone",
        'cameras': [],
        'scanning_devices': [],
        'scan_paths': [],
        'files': [],
        'scans': [],
        'analyses': [] })
    farm = factory.create("Farm", {
        "id": new_id(),
        "short_name": "valdaura",
        "name": "Valdaura Self-Sufficient Labs - Iaac Barcelona",
        "description": "Valldaura Self-sufficient Labs is a project promoted by the Institute for Advanced Architecture of Catalonia for the creation of a self-sufficient habitat research centre. Located in the Collserola Natural Park, in the heart of the metropolitan area of Barcelona, it has laboratories for the production of energy, food and things, and develops projects and academic programmes in association with leading research centres around the world.",
        "license": "CC BY-SA 4.0",
        "people": [ jonathan.serialize() ],
        "cameras": [],
        "scanning_devices": [],
        "zones": [] })

    farm.add_zone(testzone)
    db.store(farm)
    

if __name__ == "__main__":
    create_chatelain_farm()
    create_valdaura_farm()

    
