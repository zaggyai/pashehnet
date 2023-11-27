# pashehnet
Sensor network simulator publishing to MQTT broker

## Installation

If available from a package repository:
```bash
pip install pashehnet
```

Direct install from the repo:
```bash
pip install git+ssh://git@github.com/zaggyai/pashehnet
```

## Contributing

Make sure your virtual env is up-to-date:
```bash
pip install --upgrade pip wheel setuptools
```

Install package in dev/editable mode:
```bash
pip install -e .
```

Install dev environment dependencies such as `pytest`, `flake8` and supporting deps for tests:
```bash
pip install -r dev-requirements.py3
```

### Environment

You will need to define some environment variables for MQTT credentials that **_do not_** get checked into the repo:

- `MQTT_HOST` optional, defaults to `localhost`
- `MQTT_PORT` optional, defaults to `1883`
- `MQTT_USER`
- `MQTT_PWD`
- `MQTT_USE_SSL` optional, defaults to `false`

We like the cross-platform [direnv](https://direnv.net/) tool, but you do you!  :upside_down_face: