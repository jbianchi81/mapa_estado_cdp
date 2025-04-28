from a5client import Crud
import yaml
from datetime import datetime, timedelta

config = yaml.load(open("config.yml"),Loader=yaml.CLoader)

crud = Crud(config["url"], config["token"])

def getLastObs(series_id_list : list):
    timestart = datetime.now() - timedelta(days=7)
    timeend = datetime.now()
    results = []
    for id in series_id_list:
        serie = crud.readSerie(id, timestart=timestart, timeend=timeend, tipo="puntual", no_metadata=True)
        if not len(serie["observaciones"]):
            last_value = None
        else:
            last_value = serie["observaciones"][-1]["valor"]
        results.append({
            "series_id": id,
            "last_value": last_value
        })
    return results

# last_obs = getLastObs([19])
# print(yaml.dump(last_obs))