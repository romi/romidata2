#!/bin/bash

rm -rf db/

python3 demo_new_farm.py

python3 farm_import_fsdb_scan.py \
        -b db \
        --fsdb ~/projects/ROMI/Metadata/database_farmers_dashboard  \
        -P prototypes \
        -f chatelain \
        -u lettuce \
        -p guillaume \
        -t linear_4m \
        -c picamera_v2 \
        -d camera_rail  \
        1_20190416

python3 farm_import_datastream.py \
        -b db \
        -f chatelain \
        -u lettuce \
        --observable-name "Air temperature" \
        --observable-uri http://purl.oclc.org/NET/ssnx/meteo/aws#TemperatureSensor \
        --unit-name "degrees Celsius" \
        --unit-uri "http://purl.obolibrary.org/obo/UO_0000027" \
        4.json

python3 farm_import_datastream.py \
        -b db \
        -f chatelain \
        -u lettuce \
        --observable-name "Soil humidity" \
        --observable-uri http://purl.oclc.org/NET/ssnx/meteo/aws#HumiditySensor \
        --unit-name "percent" \
        --unit-uri "http://purl.obolibrary.org/obo/UO_0000027" \
        5.json

python3 farm_import_datastream.py \
        -b db \
        -f chatelain \
        -u lettuce \
        --observable-name "Sunlight (PAR)" \
        --observable-uri http://purl.oclc.org/NET/ssnx/meteo/aws#RadiationSensor \
        --unit-name "micromole/m2/s" \
        --unit-uri "xxx" \
        6.json

python3 farm_import_growth_analysis.py \
        -b db \
        -P prototypes \
        -f chatelain \
        -u lettuce \
        --start-date 2019-04-16 \
        growth_curves.txt

