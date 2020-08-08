import sys
from os.path import abspath

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.io import JsonExporter
from romidata2.db import InvestigationDatabase

if __name__ == "__main__":
    proto = Prototypes("prototypes")
    
    investigation = proto.get_investigation("ROMI")
    investigation.id = "ROMI_Tests"
    investigation.title = "ROMI Plant Phenotyping Tests"

    investigation.add_person(proto.get_person("fabfab"))
    
    db = InvestigationDatabase("db")
    db.store(investigation)

    
    
