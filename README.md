## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Config
```bash
cp config_template.yml config.yml
nano config.yml # Ingresar url y token
```
## Use

```python
from get_last_obs import getLastObsList, getLastObs, updateMapState

ultimo_valor = getLastObs(19)
ultimos_valores = getLastObsList([19, 29, 30])
mapa_actualizado = updateMapState("mapas/tramos.geojson")
updateMapState("mapas/tramos.geojson", "mapas/tramos_actualizados.geojson") 
```