import logging
import os
import sys
from functools import cache

import fire
from envyaml import EnvYAML
from schema import Schema, Optional, SchemaError

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
    SENSORS = 'sensors'
    TOPIC = 'topic'
    SOURCE = 'source'
    FORMAT = 'format'
    TRANSFORMS = 'transforms'
    ID = 'id'
    SPEC = 'spec'
    FREQUENCY = 'frequency'


@cache
def config_schema():
    """
    Returns the minimal schema required to define a network; does NOT guarantee
    that said network config will actually work as desired.
    :return: Schema object, cached
    """
    return Schema({
        ConfigKeys.VERSION: 1,
        ConfigKeys.TARGET: {
            ConfigKeys.RESOURCE: str,
            ConfigKeys.SPEC: dict
        },
        ConfigKeys.SENSORS: [{
            ConfigKeys.TOPIC: str,
            ConfigKeys.ID: str,
            Optional(ConfigKeys.FREQUENCY): int,
            ConfigKeys.SOURCE: {
                ConfigKeys.RESOURCE: str,
                ConfigKeys.SPEC: dict
            },
            ConfigKeys.FORMAT: {
                ConfigKeys.RESOURCE: str,
                ConfigKeys.SPEC: dict
            },
            Optional(ConfigKeys.TRANSFORMS): [{
                ConfigKeys.RESOURCE: str,
                ConfigKeys.SPEC: dict
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
            config = self._load_config(self.config_file)
            logging.debug(f'{ConfigKeys.VERSION}: '
                          f'{config[ConfigKeys.VERSION]}'
                          )
            logging.debug(f'{ConfigKeys.TARGET}: '
                          f'{config[ConfigKeys.TARGET][ConfigKeys.RESOURCE]}'
                          )
            logging.debug(f'{ConfigKeys.SENSORS}: '
                          f'{config[ConfigKeys.SENSORS]}'
                          )
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
