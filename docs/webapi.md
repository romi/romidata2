---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - shell

includes:
  - errors

search: false

code_clipboard: true
---

# Introduction

TODO


# Authentication

No authentication is required, yet.

# Farms

## Get All Farms

```shell
curl "http://example.com/farms"
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": "f3519ad6-e2c5-11ea-b72c-67793b3f1ad0",
    "short_name": "joes_farm",
    "name": "Joe's Farm"
  },
  {
    "id": "83ab5c68-e2bf-11ea-b72b-433b7e4259e4",
    "short_name": "jennys",
    "name": "Jenny's Organic Market Farm"
  }
]
```

This endpoint retrieves the list of all the farms in the database.

### HTTP Request

`GET http://example.com/farms`

### Query Parameters

None

## Get a Specific Farm

```shell
curl "http://example.com/farms/83ab5c68-e2bf-11ea-b72b-433b7e4259e4"
```

> The above command returns JSON structured like this:

```json
{
  "id": "83ab5c68-e2bf-11ea-b72b-433b7e4259e4",
  "short_name": "jennys",
  "name": "Jenny's Organic Market Farm",
  "description": "We're producing the tastiests organic vegetables in the valley since 1984.",
  "license": "CC BY-SA 4.0",
  "people": [
    {
      "short_name": "jenny",
      "name": "Jenny L. Sunburn",
      "email": "Jenny.Sunburn@example.com",
      "affiliation": "",
      "id": "012c01a0-e2c6-11ea-9b85-cbc02e75d84b",
      "role": "Crop Manager"
    }
  ],
  "zones": [
    {
      "id": "9a9722d6-e2bf-11ea-82c8-e30ab21915dc",
      "short_name": "parcel_south"
    }
  ]
}
```

This endpoint retrieves data of a specific farm. The returned data
includes the following fields:

Field | Description
----- | ----------- 
`id` | The IDs of the farm.
`short_name`, `name`, `description` | The short name, the free-form, long name, and a longer description of the farm.
`people` | The list of people associated with this farm.
`zones` | The list of zones defined by this farm.


### HTTP Request

`GET http://example.com/farms/<FarmID>`

### URL Parameters


Parameter | Description
--------- | -----------
FarmID | The ID of the farm


# Zones

A zone is an area in the farm. There is no specification on how small
or how large a zone should be. It is up to the farmer's discretion to
organise the farm into zones. 


## Get a Specific Zone

```shell
curl "http://example.com/zones/9a9722d6-e2bf-11ea-82c8-e30ab21915dc"
```

> The above command returns JSON structured like this:

```json
{
  "id": "9a9722d6-e2bf-11ea-82c8-e30ab21915dc",
  "farm": "83ab5c68-e2bf-11ea-b72b-433b7e4259e4",
  "short_name": "parcel_south",
  "scans": [
    {
      "id": "bf0d485c-e2bf-11ea-b145-737f5dd43c7b",
      "date": "2019-04-16T12:00:00+02:00"
    },
    {
      "id": "bf61a8a2-e2bf-11ea-844a-0f6f68e88696",
      "date": "2019-04-17T12:00:00+02:00"
    },
    {
      "id": "bfab8b66-e2bf-11ea-a0a6-f3656e05228a",
      "date": "2019-04-18T12:00:00+02:00"
    }
  ]
}
```

This endpoint retrieves data of a specific farm. The returned data
includes the following fields:

Field | Description
----- | ----------- 
`id` `farm` | The IDs of the zone and farm, respectively.
`short_name` | The short name of the zone.
`scans` | The list of scans performed in this zone.



### HTTP Request

`GET http://example.com/zones/<ZoneID>`

### URL Parameters

Parameter | Description
--------- | -----------
ZoneID | The ID of the zone


# Scans

Scans are a special operation inside a zone. Using a scanning device
(drone, cablebot, rover, handheld camera...), a series of images is
taken in the zone. These images can then be analysed to extract useful
information, such as the list of individual plants and their sizes.

## Get a Specific Scan

```shell
curl "http://example.com/scans/bf0d485c-e2bf-11ea-b145-737f5dd43c7b"
```

> The above command returns JSON structured like this:

```json
{
  "id": "bf0d485c-e2bf-11ea-b145-737f5dd43c7b",
  "zone": "9a9722d6-e2bf-11ea-82c8-e30ab21915dc",
  "farm": "83ab5c68-e2bf-11ea-b72b-433b7e4259e4",
  "date": "2019-04-16T12:00:00+02:00",
  "images": [
    "331f229e-e2c3-11ea-a637-87b6109b19f5",
    "336dc4da-e2c3-11ea-bb69-3bcb75a2a6c8",
    "..."
  ],
  "locations": [
    "scanpath": "TODO"
  ],
  "analyses": [
    {
      "id": "fa11ec46-e2bf-11ea-8a05-737da99a972a",
      "short_name": "stitching",
      "name": "2D image stitching",
      "state": "Finished"
    },
    {
      "id": "fa625276-e2bf-11ea-82f6-e71b67ec1d85",
      "short_name": "plant_analysis",
      "name": "Plant Analysis",
      "state": "Finished"
    }
  ],
  "datastreams": [
    {
      "id": "fa11ec46-e2bf-11ea-8a05-737da99a972a",
      "short_name": "stitching",
      "name": "2D image stitching",
      "state": "Finished"
    },
    {
      "id": "fa625276-e2bf-11ea-82f6-e71b67ec1d85",
      "short_name": "plant_analysis",
      "name": "Plant Analysis",
      "state": "Finished"
    }
  ]
}
```

This endpoint retrieves data of a specific scan that was performed of a zone. The returned data includes the following fields:

Field | Description
----- | ----------- 
`id`, `zone`, `farm` | The IDs of the analysis, zone, and farm, respectively.
`data` | The date at which the scan was taken, in the ISO 8601 format.
`images` | An array with the IDs of all the images that were taking during the scan.
`analyses` | An array with all the analyses that have been performed using the scan data.


For farms, the following two analysis are noteworthy:

Short Name     | Description
-------------- | ----------- 
stitching      | This analysis stitches all the images into one single, large image of the zone. 
plant_analysis | The analysis detects the individual plants and their positions, and gives them a unique ID throughout subsequent scans.

Both analyses are detaild further below.


### HTTP Request

`GET http://example.com/scans/<ScanID>`

### URL Parameters

Parameter | Description
--------- | -----------
ScanID | The ID of the scan


# Analyses

Analysis provide useful information for a zone. In many cases, the
analyses use the image data of a scan (directly or indirectly).


## Get a Specific Analysis

```shell
curl "http://example.com/analyses/fa11ec46-e2bf-11ea-8a05-737da99a972a"
```

> The above command returns JSON structured like this:

```json
{
  "id": "fa11ec46-e2bf-11ea-8a05-737da99a972a",
  "short_name": "stitching",
  "name": "2D image stitching",
  "description": "...",
  "state": "Finished",
  "results": {}
}
```

This endpoint retrieves data of a specific analysis. The returned data
includes the following fields:

Field | Description
----- | ----------- 
`id` | The immutable ID of the analysis.
`short_name`, `name`, `description` | The short name, the free-form, long name, and a longer description.
`state` | The state of the analysis. Can be one of "Defined", "Running", "Finished", or "Error".
`results` | A JSON dictionnary that contains the analysis-specific results of the analysis.

### HTTP Request

`GET http://example.com/farms/analyses/<AnalysisID>`

### URL Parameters

Parameter | Description
--------- | -----------
FarmID | The ID of the farm
ZoneID | The ID of the zone
AnalysisID | The ID of the analysis


## The `stitching` analysis

> The stitching analysis returns JSON structured like this:

```json
{
  "id": "esk57bkz",
  "short_name": "stitching",
  "name": "2D image stitching",
  "description": "...",
  "state": "Finished",
  "results": {
    "map": "hwolyikg",
    "width": 2300,
    "height": 8609,
    "mask": "g4iifvr9"
  }
}
```

The `results` section of a stitching analysis contains the following data:

Field | Description
----- | ----------- 
`map` | The ID of the stitched image.
`mask` | The ID of the black-and-white stitched image mask (plants: white, soil: black).
`width`, `height` | The width and height of the map and mask.


## The `plant_analysis` data

> The `plant_analysis` returns JSON structured like this:

```json
{
  "id": "wg44993j",
  "short_name": "plant_analysis",
  "name": "Plant Analysis",
  "description": "...",
  "state": "Finished",
  "results": {
    "plants": [
      {
        "image": "wrdbyald",
        "location": [
          277.70588235294116,
          5696.176470588235
        ],
        "id": "0",
        "PLA": 409.18415625,
        "mask": "bgg35jv8"
      },
      {
        "image": "3yhukq53",
        "location": [
          1381.2307692307693,
          5656.4358974358975
        ],
        "id": "1",
        "PLA": 1088.7001875,
        "mask": "qxl3dtpj"
      },
      {
        "image": "...",
        "location": [],
        "id": "..",
        "PLA": 0,
        "mask": "..."
      }
    ]
  }
}
```

The results section of the plant analysis contains the `plants` array
with information on all the plants that were detected in the scan. For
each plant, the following data is available:

Field | Description
----- | ----------- 
`id` | The unique ID of the plant.
`image`, `mask` | The cropped image of the plant and its mask.
`location` | The x and y offset of the plant in the stitched map, in pixels.
`PLA` | The Projected Leaf Area (PLA) the plant in pixels. The PLA is a proxy measure of the plants size.


# Images


## Get an Image

```shell
curl "http://example.com/images/95vaybgy/jxjecsik/3yhukq53?size=thumb"
```

> The above command returns the image scaled to the requested size.


### HTTP Request

`GET http://example.com/images/<ImageID>`

`GET http://example.com/images/<ImageID>?size=<SizeLabel>&orientation=<OrientationLabel>&direction=<DirectionLabel>`

### URL Parameters

Parameter | Description
--------- | -----------
ImageID | The ID of the image

### Query Parameters

Parameter | Default | Description
--------- | ------- | -----------
size | thumb | Defines the size of the image to be returned. The following options are currently available: 'thumb' (max. 150x150), 'large' (max. 1500x1500), and 'orig' (original size).
orientation | orig | Defines the orientation of the image to be returned. The following options are currently available: 'orig' (no changes), 'horizontal' (width > height), and 'vertical' (height > width).
direction | cw | Defines the direction to rotate the image, if needed. The following options are currently available: 'cw' (clock-wise) and 'ccw' (counter-clock-wise)
