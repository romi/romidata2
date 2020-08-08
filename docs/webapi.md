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
    "id": "dszphw4i",
    "short_name": "joes_farm",
    "name": "Joe's Farm"
  },
  {
    "id": "95vaybgy",
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
curl "http://example.com/farms/95vaybgy"
```

> The above command returns JSON structured like this:

```json
{
  "id": "95vaybgy",
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
      "id": "cxjqd5z0",
      "role": "Crop Manager"
    }
  ],
  "zones": [
    {
      "id": "jxjecsik",
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
curl "http://example.com/farms/95vaybgy/zones/jxjecsik"
```

> The above command returns JSON structured like this:

```json
{
  "id": "jxjecsik",
  "farm": "95vaybgy",
  "short_name": "parcel_south",
  "scans": [
    {
      "id": "lddu2z2k",
      "date": "2019-04-16T12:00:00+02:00"
    },
    {
      "id": "msyjy6ar",
      "date": "2019-04-17T12:00:00+02:00"
    },
    {
      "id": "ribqb9he",
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

`GET http://example.com/farms/<FarmID>/zones/<ZoneID>`

### URL Parameters

Parameter | Description
--------- | -----------
FarmID | The ID of the farm
ZoneID | The ID of the zone


# Scans

Scans are a special operation inside a zone. Using a scanning device
(drone, cablebot, rover, handheld camera...), a series of images is
taken in the zone. These images can then be analysed to extract useful
information, such as the list of individual plants and their sizes.

## Get a Specific Scan

```shell
curl "http://example.com/farms/95vaybgy/zones/jxjecsik/scans/lddu2z2k"
```

> The above command returns JSON structured like this:

```json
{
  "id": "lddu2z2k",
  "farm": "95vaybgy",
  "zone": "jxjecsik",
  "date": "2019-04-16T12:00:00+02:00",
  "images": [
    "fls2y871",
    "8c6xc9c7",
    "59djet16",
    "..."
  ],
  "locations": [
    "scanpath": "TODO"
  ],
  "analyses": [
    {
      "id": "esk57bkz",
      "short_name": "stitching",
      "name": "2D image stitching",
      "state": "Finished"
    },
    {
      "id": "wg44993j",
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

`GET http://example.com/farms/<FarmID>/zones/<ZoneID>/scans/<ScanID>`

### URL Parameters

Parameter | Description
--------- | -----------
FarmID | The ID of the farm
ZoneID | The ID of the zone
ScanID | The ID of the scan


# Analyses

Analysis provide useful information for a zone. In many cases, the
analyses use the image data of a scan (directly or indirectly).


## Get a Specific Analysis

```shell
curl "http://example.com/farms/95vaybgy/zones/jxjecsik/scans/lddu2z2k"
```

> The above command returns JSON structured like this:

```json
{
  "id": "esk57bkz",
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

`GET http://example.com/farms/<FarmID>/zones/<ZoneID>/analyses/<AnalysisID>`

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

All images of the scans and all images produced by various analyses
are stored per zone. To uniquely identify an image, you need the
farm ID, the zone ID, and the image ID.

## Get an Image

```shell
curl "http://example.com/images/95vaybgy/jxjecsik/3yhukq53?size=thumb"
```

> The above command returns the image scaled to the requested size.


### HTTP Request

`GET http://example.com/images/<FarmID>/<ZoneID>/<ImageID>`

### URL Parameters

Parameter | Description
--------- | -----------
FarmID | The ID of the farm
ZoneID | The ID of the zone
ImageID | The ID of the image

### Query Parameters

Parameter | Default | Description
--------- | ------- | -----------
size | thumb | Defines the size of the image to be returned. The following options are currently available: 'thumb' (max. 150x150), 'large' (max. 1500x1500), and 'orig' (original size).
