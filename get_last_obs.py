from a5client import Crud
import yaml
from datetime import datetime, timedelta
import json
import logging

config = yaml.load(open("config.yml"),Loader=yaml.CLoader)

crud = Crud(config["url"], config["token"])

def getLastObsList(series_id_list : list):
    results = []
    for series_id in series_id_list:
        last_value = getLastObs(series_id)
        results.append({
            "series_id": series_id,
            "last_value": last_value
        })
    return results

def getLastObs(series_id : int, timestart : datetime = datetime.now() - timedelta(days=7), timeend : datetime = datetime.now()):
    serie = crud.readSerie(series_id, timestart=timestart, timeend=timeend, tipo="puntual", no_metadata=True)
    if not len(serie["observaciones"]):
        return None
    else:
        return serie["observaciones"][-1]["valor"]

def updateMapState(mapfile : str, outputfile : str = None):
    tramos_geojson = json.load(open(mapfile,"r",encoding="utf-8"))
    for i, feature in enumerate(tramos_geojson["features"]):
        if "series_id" not in feature["properties"]:
            logging.error("Falta propiedad 'series_id' en el feature %i" % i)
            continue
        series_id = int(feature["properties"]["series_id"])
        last_value = getLastObs(series_id)
        feature["properties"]["valor"] = last_value
        estado = getState(series_id, last_value)
        feature["properties"]["estado"] = estado
    if outputfile is not None:
        json.dump(tramos_geojson, open(outputfile,"w", encoding="utf-8"))
    else:
        return tramos_geojson

def getState(series_id, valor):
    # TODO
    return "normal"

