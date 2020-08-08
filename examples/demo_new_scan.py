import sys
from os.path import abspath

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.db import InvestigationDatabase

if __name__ == "__main__":
    proto = Prototypes("prototypes")
    
    db = InvestigationDatabase("db")
    investigation = db.get("ROMI_Tests")
    study = investigation.get_study("vplants")

    # Let's scan the first plant
    plant = study.observation_units[0]

    scan = study.new_scan(person_names = ["fabfab"],
                          observation_unit_id = plant.id)
    

    print(study.id)

    # Scan the second plant
    plant = study.observation_units[1]
    newscan = study.clone_scan(scan)
    newscan.observation_unit_id = plant.id
    
    db.store(investigation)
