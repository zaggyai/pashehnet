# PashehNet
Provides a simulated sensor network (SSN) framework for publishing to a target 
system.  The package implements both an API and command line interface to provide 
this service.

This README is intentionally short for tl;dr purposes.  Full documentation can be found [here](https://pashehnet.readthedocs.io).

## Installation

If available from a package repository:
```bash
pip install pashehnet
```

Otherwise you can install directly from the GitHub repo:
```bash
pip install git+https://github.com/zaggyai/pashehnet
```

## Contributing

First, fork the repo if not a current maintainer, or clone if you are!  :)

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
pip install -r dev-requirements.txt
```

Keep in mind that even if you already have a virtualenv configured from a previous 
fork/clone, its dependencies could be out of date so re-running the installs should 
bring your virtualenv current.

### Environment

You can leverage environment variables within code or CLI config files for sensitive 
data you don't want to check into a repo.  This is always a going concern for any code
that requires client/server configuration.  **Please be careful to never add security 
credentials to a commit** as they're nearly impossible to permanently remove from a repo after 
the fact.

For MQTT broker config, we typically define the following env vars and use them in our code/configs:

- `MQTT_HOST`
- `MQTT_PORT`
- `MQTT_USER`
- `MQTT_PWD`

We like the cross-platform [direnv](https://direnv.net/) tool and have a gitignore exclusion for 
its files, but you do you!  :upside_down_face:

### Opening a Pull Request (PR)

Pull requests are a git workflow for managing branch merges with reviews and 
tests.  You can read more about them in the [GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).  Before opening a PR 
please make sure the following commands complete locally without errors in your 
local dev environment as they will block a PR if not:

```bash
# Run linter
flake8 src/ tests/

# Run all unit tests
# Note we disable deprecation warnings for the time being;
# there's a method to the madness
pytest -W ignore::DeprecationWarning
```
