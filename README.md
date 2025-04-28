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
from get_last_obs import getLastObs

last_values = getLastObs([19, 29, 30])
```