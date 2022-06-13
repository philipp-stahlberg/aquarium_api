# Overview

Simple prototype REST-API to monitor/manage multiple resources for aquariums.


## Short resource descriptions: 

Aquarium:
- has properties name, volume, measured temperatures and fertilization.

Temperature:
- measured temperature for a single aquarium

Fertilization:
- consists a fertilizer which is used with a specific amount for an aquarium

Fertilizer:
- usable fertilizer that can contain different chemicals

Chemical:
- unique name description for a chemical that can be in a fertilizer

# Usage 
## Get a list of aquariums

### Request

`GET /aquariums`

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums

#### Order by name ascending/descending

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums?order-by=name:asc
    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums?order-by=name:desc

#### Order by liter ascending/descending

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums?order-by=liter:asc
    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums?order-by=liter:desc

## Create new aquarium

`POST /aquariums`

    curl -i -H 'Content-Type: application/json' -d '{"name":"my_aquarium","volume_in_liter":200.0}' http://localhost:5000/aquariums

## Get single aquarium

`GET /aquariums/<id>`

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/aquariums/1

## Edit existing aquarium

`PATCH /aquariums/<id>`

    curl -i -H 'Content-Type: application/json' -d '{"id":1,"name":"new_aquarium_name","volume_in_liter":200.0}' -X PATCH http://localhost:5000/aquariums/1

## Delete existing aquarium

`DELETE /aquariums/<id>`

     curl -i -X DELETE http://localhost:5000/aquariums/1 

## Get list of temperatures

`GET /temperatures`

    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures

#### Order by celsius ascending/descending
    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures?order-by=celsius:asc
    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures?order-by=celsius:desc

#### Order by date ascending/descending
    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures?order-by=date:asc
    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures?order-by=date:desc

## Create new temperature for aquarium with id

`POST /temperatures`

    curl -i -H 'Content-Type: application/json' -d '{"celsius": 21.1, "aquarium_id": 3}' http://localhost:5000/temperatures

## Get single temperature

`GET /temperatures/<id>`

    curl -i -H 'Accept: application/json' http://localhost:5000/temperatures/1

## Delete temperature

`DELETE /temperatures/<id>`

    curl -i -X DELETE http://localhost:5000/temperatures/1

## Get list of chemicals

`GET /chemicals`

    curl -i -H 'Accept: application/json' http://localhost:5000/chemicals

#### Order by name ascending/descending

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/chemicals?order-by=name:asc
    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/chemicals?order-by=name:desc

## Create new chemical
`POST /chemicals`

    curl -i -H 'Content-Type: application/json' -d '{"name": "iron"}' http://localhost:5000/chemicals

## Get single chemical

`GET /chemicals/<id>`

    curl -i -H 'Accept: application/json' http://localhost:5000/chemicals/1

## Edit existing chemical

`PATCH /chemicals/<id>`

    curl -i -H 'Content-Type: application/json' -d '{"id":1,"name":"updated_name"}' -X PATCH http://localhost:5000/chemicals/1

## Delete chemical

`DELETE /chemicals/<id>`

    curl -i -X DELETE http://localhost:5000/chemicals/1

## Get list of fertilizer

`GET /fertilizers`

    curl -i -H 'Accept: application/json' http://localhost:5000/fertilizers

#### Order by name ascending/descending

    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/fertilizers?order-by=name:asc
    curl -i -H 'Accept: application/json' http://127.0.0.1:5000/fertilizers?order-by=name:desc

## Create new fertilizer
`POST /fertilizers`

    curl -i -H 'Content-Type: application/json' -d '{"name": "fertilizer_name"}' http://localhost:5000/fertilizers

## Get single fertilizer

`GET /fertilizers/<id>`

    curl -i -H 'Accept: application/json' http://localhost:5000/fertilizers/1

## Edit existing fertilizer

`PATCH /fertilizers/<id>`

    curl -i -H 'Content-Type: application/json' -d '{"id":1,"name":"updated_name", "chemicals": [1,2]}' -X PATCH http://localhost:5000/fertilizers/1

## Delete fertilizer

`DELETE /fertilizers/<id>`

    curl -i -X DELETE http://localhost:5000/fertilizers/1

## Get list of fertilization

`GET /fertilization`

    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization

#### Order by amount ascending/descending
    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization?order-by=amount:asc
    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization?order-by=amount:desc

#### Order by date ascending/descending
    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization?order-by=date:asc
    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization?order-by=date:desc

## Create new fertilization
`POST /fertilization`

    curl -i -H 'Content-Type: application/json' -d '{"amount_in_milliliter": 5, "aquarium_id": 1, "fertilizer_id": 1}' http://localhost:5000/fertilization

## Get single fertilization

`GET /fertilization/<id>`

    curl -i -H 'Accept: application/json' http://localhost:5000/fertilization/1

## Edit existing fertilization

`PATCH /fertilization/<id>`

    curl -i -H 'Content-Type: application/json' -d '{"id":1,"amount_in_milliliter": 5, "aquarium_id": 1, "fertilizer_id": 1}' -X PATCH http://localhost:5000/fertilization/1

## Delete fertilization

`DELETE /fertilization/<id>`

    curl -i -X DELETE http://localhost:5000/fertilization/1

