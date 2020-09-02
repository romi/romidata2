
from romidata2.datamodel import *
from romidata2.impl import current_date

def new_scan(db: IDatabase,
             factory: IFactory,
             observation_unit_id: str,
             person_ids: List[str],
             camera_id: str,
             scanning_device_id: str,
             scan_path: IScanPath) -> IScan:

    observation_unit = db.lookup(observation_unit_id)
    if observation_unit.classname != "ObservationUnit":
        raise ValueError("Invalid observation unit ID")
        
    farm_or_study = observation_unit.context
    print(observation_unit.serialize())
    print(farm_or_study.serialize())
    
    people = []
    for person_id in person_ids:
        person = farm_or_study.get_person(person_id)
        if not person:
            raise ValueError("Invalid person ID")
        people.append(person)

    camera = farm_or_study.get_camera(camera_id)
    if not camera:
        raise ValueError("Invalid camera ID")

    scanning_device = farm_or_study.get_scanning_device(scanning_device_id)
    if not scanning_device:
        raise ValueError("Invalid scanning device ID")
    
    scan = factory.create("Scan", {
        "observation_unit": observation_unit.id,
        "date": current_date().isoformat(),
        "people": [p.id for p in people],
        "camera": camera.id,
        "scanning_device": scanning_device.id,
        "scan_path": scan_path.serialize(),
        "factor_values": {}
    })

    observation_unit.add_scan(scan)

    return scan
