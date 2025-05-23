# from a5client import Crud
# import yaml
# from datetime import datetime, timedelta
import json
import logging
import requests
import argparse

# config = yaml.load(open("config.yml"),Loader=yaml.CLoader)

# crud = Crud(config["url"], config["token"])

# def getLastObsList(series_id_list : list):
#     results = []
#     for series_id in series_id_list:
#         last_value = getLastObs(series_id)
#         results.append({
#             "series_id": series_id,
#             "last_value": last_value
#         })
#     return results

# def getLastObs(series_id : int, timestart : datetime = datetime.now() - timedelta(days=7), timeend : datetime = datetime.now()):
#     serie = crud.readSerie(series_id, timestart=timestart, timeend=timeend, tipo="puntual", no_metadata=True)
#     if not len(serie["observaciones"]):
#         return None
#     else:
#         return serie["observaciones"][-1]["valor"]

# def updateMapState(mapfile : str, outputfile : str = None):
#     tramos_geojson = json.load(open(mapfile,"r",encoding="utf-8"))
#     for i, feature in enumerate(tramos_geojson["features"]):
#         if "series_id" not in feature["properties"]:
#             logging.error("Falta propiedad 'series_id' en el feature %i" % i)
#             continue
#         series_id = int(feature["properties"]["series_id"])
#         last_value = getLastObs(series_id)
#         feature["properties"]["valor"] = last_value
#         estado = getState(series_id, last_value)
#         feature["properties"]["estado"] = estado
#     if outputfile is not None:
#         json.dump(tramos_geojson, open(outputfile,"w", encoding="utf-8"))
#     else:
#         return tramos_geojson

def findFeature(geojson : dict, series_id : int):
    for feature in geojson["features"]:
        if feature["properties"]["series_id"] == series_id:
            return feature
    raise ValueError("feature with series_id=%i not found" % series_id)

def updateMapStateFromGeoserver(mapfile : str, outputfile : str = None):
    tramos_geojson = json.load(open(mapfile,"r",encoding="utf-8"))
    ultimas_alturas = getUltimasAlturasGeoserver()
    ultimos_caudales = getUltimosCaudalesGeoserver()
    for i, feature in enumerate(tramos_geojson["features"]):
        if "series_id" not in feature["properties"]:
            logging.error("Falta propiedad 'series_id' en el feature %i" % i)
            continue
        series_id = int(feature["properties"]["series_id"])
        if feature["properties"]["var_id"] == 4:
            last_values_feature = findFeature(ultimos_caudales, series_id) 
        else:
            last_values_feature = findFeature(ultimas_alturas, series_id)
        feature["properties"]["valor"] = last_values_feature["properties"]["valor"]
        feature["properties"]["estado"] = getState(last_values_feature["properties"]["percentil"])
    if outputfile is not None:
        json.dump(tramos_geojson, open(outputfile,"w", encoding="utf-8"), ensure_ascii=False)
    else:
        return tramos_geojson


def getOwsLayer(
        url : str = "https://alerta.ina.gob.ar/geoserver/ows", 
        layer_name : str = "siyah:ultimas_alturas_con_timeseries", 
        params : dict = {
                "service": 'WFS',
                "version": '1.0.0',
                "request": 'GetFeature',
                # "typeName": layer_name,
                "maxFeatures": '500',
                "outputFormat": 'application/json'
            }):
    params = {**params, "typeName": layer_name}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def getUltimasAlturasGeoserver():
    return getOwsLayer(layer_name="ultimas_alturas_con_timeseries")

def getUltimosCaudalesGeoserver():
    return getOwsLayer(layer_name="ultimos_caudales_con_timeseries")

def getState(percentil):
    if percentil is None:
        return ""
    if percentil not in status_categories:
        raise ValueError("Percentil %i not found in mapping table" % percentil)
    return status_categories[percentil]

status_categories : dict = {
    5: "aguas altas",
    25: "aguas medias altas",
    50: "aguas medias",
    75: "aguas medias",
    95: "aguas medias bajas",
    100: "aguas bajas"
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Actualiza mapa con últimos valores y estado")
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='mapas/tramos_actualizados.geojson',
        help='Path to output file (default= mapas/tramos_actualizados.geojson)',
    )

    # Input path with default value
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='mapas/tramos.geojson',
        help='Path to input file (default: mapas/tramos.geojson)'
    )

    args = parser.parse_args()
    updateMapStateFromGeoserver(args.input, args.output)