## Instalación
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Uso básico en consola de python

```python
from get_last_obs import updateMapStateFromGeoserver

updateMapStateFromGeoserver("mapas/tramos.geojson", "mapas/tramos_actualizados.geojson") 
```
## O desde bash
```bash
python get_last_obs.py -i mapas/tramos.geojson -o mapas/tramos_actualizados.geojson
```
