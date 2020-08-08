import sys
from os.path import abspath
import datetime

sys.path.append(abspath('..'))
from romidata2.protodb import Prototypes
from romidata2.db import InvestigationDatabase

if __name__ == "__main__":
    proto = Prototypes("prototypes")
    
    db = InvestigationDatabase("db")
    investigation = db.get("ROMI_Tests")

    study = proto.get_study("empty")
    study.id = "vplants"
    study.title = "Virtual Plants"
    study.description = "Testing the pipeline on virtual plants"
    study.add_person(proto.get_person("fabfab"))
    study.add_camera(proto.get_camera("virtual_camera"))
    study.add_scanning_device(proto.get_scanning_device("virtual_scanner"))
    study.add_experimental_factor(proto.get_experimental_factor("genotype_ahp6_mutation"))
    study.add_scan_path(proto.get_scan_path("circular_36"))

    # Add all the wildtype plants used in the study
    plant_proto = proto.get_observation_unit("RDP:186AV.L1:plantID:date:WT")

    today = datetime.date.today()
    for n in range(1, 50):
        plant = plant_proto.clone()
        plant.id = "RDP:186AV.L1:%03d:%04d%02d%02d:WT" % (n, today.year,
                                                          today.month, today.day)
        study.add_observation_unit(plant)

    # Add all the mutant plants used in the study
    plant_proto = proto.get_observation_unit("RDP:186AV.L1:plantID:date:ahp6")

    today = datetime.date.today()
    for n in range(1, 50):
        plant = plant_proto.clone()
        plant.id = "RDP:186AV.L1:%03d:%04d%02d%02d:ahp6" % (n, today.year,
                                                            today.month, today.day)
        study.add_observation_unit(plant)

    investigation.add_study(study)
    db.store(investigation)
