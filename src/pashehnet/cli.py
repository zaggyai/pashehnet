import logging
import os
import sys
from functools import lru_cache

import fire
from envyaml import EnvYAML
from schema import Schema, Optional, SchemaError, Or

from pashehnet.network import SensorNetwork

import pashehnet.targets
import pashehnet.sensors.sources
import pashehnet.sensors.formats
import pashehnet.sensors.transforms
from pashehnet.sensors import Sensor


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
    """
    Because typos in string literal keys happen
    """
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


@lru_cache
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
            Optional(ConfigKeys.FREQUENCY): Or(int, float),
            ConfigKeys.SOURCE: {
                ConfigKeys.RESOURCE: str,
                Optional(ConfigKeys.SPEC): dict
            },
            ConfigKeys.FORMAT: {
                ConfigKeys.RESOURCE: str,
                Optional(ConfigKeys.SPEC): dict
            },
            Optional(ConfigKeys.TRANSFORMS): [{
                ConfigKeys.RESOURCE: str,
                Optional(ConfigKeys.SPEC): dict
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
            logging.debug('Creating target from spec')
            target = self._target_from_config(config[ConfigKeys.TARGET])
            logging.debug('Creating sensor network')
            network = SensorNetwork(target)
            logging.debug('Adding sensors...')
            self._sensors_from_config(network, config[ConfigKeys.SENSORS])
            logging.debug('Network populated, starting up')
            network.start()
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

    def _target_from_config(self, target_cfg):
        """
        Instantiate network target from config

        :param target_cfg: Target section of config file
        """
        cls = target_cfg[ConfigKeys.RESOURCE]
        kwargs = target_cfg.get(ConfigKeys.SPEC, {})
        return vars(pashehnet.targets)[cls](**kwargs)

    def _sensors_from_config(self, network, sensors_cfg):
        """
        Instantiate network sensors from config

        :param sensors_cfg: Sensors section of config file
        """
        for spec in sensors_cfg:
            topic = spec[ConfigKeys.TOPIC]
            id = spec[ConfigKeys.ID]
            logging.debug(f'Adding sensor id: {id} // topic: {topic}')
            freq = spec[ConfigKeys.FREQUENCY]
            source = self._source_from_config(spec[ConfigKeys.SOURCE])
            format = self._format_from_config(spec[ConfigKeys.FORMAT])
            transforms = [
                self._transform_from_config(cfg)
                for cfg in spec.get(ConfigKeys.TRANSFORMS, [])
            ]
            sensor = Sensor(id, source, format, transforms, freq)
            network.add_sensor(topic, sensor)

    def _source_from_config(self, source_cfg):
        """
        Instantiate sensor source from config

        :param source_cfg: Sensor source section of config file
        """
        cls = source_cfg[ConfigKeys.RESOURCE]
        kwargs = source_cfg.get(ConfigKeys.SPEC, {})
        return vars(pashehnet.sensors.sources)[cls](**kwargs)

    def _format_from_config(self, format_cfg):
        """
        Instantiate sensor format from config

        :param format_cfg: Sensor format section of config file
        """
        cls = format_cfg[ConfigKeys.RESOURCE]
        kwargs = format_cfg.get(ConfigKeys.SPEC, {})
        return vars(pashehnet.sensors.formats)[cls](**kwargs)

    def _transform_from_config(self, xform_config):
        """
        Instantiate sensor transform from config

        :param xform_config: Sensor transform item from config file
        """
        cls = xform_config[ConfigKeys.RESOURCE]
        kwargs = xform_config.get(ConfigKeys.SPEC, {})
        return vars(pashehnet.sensors.transforms)[cls](**kwargs)


def cli_main():
    fire.Fire(Runner)


if __name__ == '__main__':
    cli_main()
