import logging
import os
import sys
from functools import cache

import fire
from envyaml import EnvYAML
from schema import Schema, Optional, Use, And, SchemaError

########################################
# Set up logging
########################################
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logging.getLogger().setLevel(
    logging.getLevelName(
        os.getenv('LOG_LEVEL', 'WARN').upper()
    )
)


class ConfigurationError(Exception):
    pass


class ConfigKeys:
    VERSION = 'version'
    TARGET = 'target'
    RESOURCE = 'resource'
    SPEC = 'spec'
    SENSORS = 'sensors'
    TOPIC = 'topic'
    SOURCE = 'source'
    FORMAT = 'format'
    ID = 'id'

@cache
def config_schema():
    """
    Returns the minimal schema required to define a network; does NOT guarantee
    that said network config will actually work as desired.
    :return: Schema object, cached
    """
    return Schema({
        'version': 1,
        'target': {
            'resource': str,
            'spec': dict
        },
        'sensors': [{
            'topic': str,
            'id': str,
            Optional('frequency'): int,
            'source': {
                'resource': str,
                'spec': dict
            },
            'format': {
                'resource': str,
                'spec': dict
            },
            Optional('transforms'): [{
                'resource': str,
                'spec': dict
            }]
        }],
        str: object  # Catchall as we don't care about extra cruft
    })


class Runner(object):
    """
    Provides a wrapper to create the network and kick off the simulation from
    a command line interface
    """
    CURRENT_CONFIG_VERSION = 1
    DEFAULT_CONFIG_FNAME = 'config.yaml'

    def __init__(self, config=DEFAULT_CONFIG_FNAME):
        """
        :param config_fname: Network configuration filename
        """
        self.config_file = config

    def run(self):
        """
        Create and run the network simulation
        :return: None
        """
        logging.debug('Starting runner')
        try:
            config = self._load_config(self.config_file)  # noqa: F841
        except Exception as e:
            logging.error(e)

    def check(self):
        """
        Load and validate network configuration, without creating or running it
        :return: None
        """
        logging.debug('Starting configuration check')
        try:
            config = self._load_config(self.config_file)  # noqa: F841
            logging.debug(f'{ConfigKeys.VERSION}: {config[ConfigKeys.VERSION]}')
            logging.debug(f'{ConfigKeys.TARGET}: {config[ConfigKeys.TARGET][ConfigKeys.RESOURCE]}')
            logging.debug(f'{ConfigKeys.SENSORS}: {config[ConfigKeys.SENSORS]}')
        except Exception as e:
            logging.error(e)

    @staticmethod
    def _load_config(config_file):
        """
        Load and validate the given configuration filename
        :param config_fname: Network configuration filename
        :return: Loaded config
        """
        logging.debug(f'Loading configuration file: {config_file}')
        try:
            config = EnvYAML(config_file).export()
            config_schema().validate(config)
            return config
        except SchemaError as e:
            raise ConfigurationError(str(e))
        except Exception as e:
            raise ConfigurationError(str(e))


def cli_main():
    fire.Fire(Runner)
