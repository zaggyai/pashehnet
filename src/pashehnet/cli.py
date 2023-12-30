"""
This module provides the command line interface via `pashehnet` that allows a
user to launch a simulated sensor network via a provided YAML configuration
file.
"""
import logging
import os
import sys
from functools import lru_cache
from importlib import import_module

import fire
from envyaml import EnvYAML
from schema import Schema, Optional, SchemaError, Or

import pashehnet.sensors.formats
import pashehnet.sensors.sources
import pashehnet.sensors.transforms
import pashehnet.targets
from pashehnet.network import SensorNetwork
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
    """
    Custom exception raised when a configuration file error is encountered.
    """
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
            logging.info('Creating target from spec')
            target = self._target_from_config(config[ConfigKeys.TARGET])
            logging.info('Creating sensor network')
            network = SensorNetwork(target)
            logging.info('Adding sensors...')
            self._sensors_from_config(network, config[ConfigKeys.SENSORS])
            logging.info('Network populated, starting up...')
            network.start()
            logging.info('Network running')
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
        return self._instantiate_obj(pashehnet.targets, cls, kwargs)

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
        return self._instantiate_obj(pashehnet.sensors.sources, cls, kwargs)

    def _format_from_config(self, format_cfg):
        """
        Instantiate sensor format from config

        :param format_cfg: Sensor format section of config file
        """
        cls = format_cfg[ConfigKeys.RESOURCE]
        kwargs = format_cfg.get(ConfigKeys.SPEC, {})
        return self._instantiate_obj(pashehnet.sensors.formats, cls, kwargs)

    def _transform_from_config(self, xform_config):
        """
        Instantiate sensor transform from config

        :param xform_config: Sensor transform item from config file
        """
        cls = xform_config[ConfigKeys.RESOURCE]
        kwargs = xform_config.get(ConfigKeys.SPEC, {})
        return self._instantiate_obj(pashehnet.sensors.transforms, cls, kwargs)

    def _instantiate_obj(self, core_pkg, cls, kwargs):
        """
        Util method to wrap common dynamic module load/instantiation logic

        :param core_pkg:
        :param cls:
        :param kwargs:
        :return:
        """
        try:
            # Try happy path where it's a core class
            obj = vars(core_pkg)[cls](**kwargs)
            return obj
        except:  # noqa: E722
            logging.debug(
                f'{cls} not found in core packages, '
                f'checking for external module'
            )

        # Now try the less happy path, see if it's a custom module
        parts = cls.split('.')
        pkg = '.'.join(parts[:-1])
        cls = parts[-1]
        m = import_module(pkg)
        return vars(m)[cls](**kwargs)


def cli_main():
    """
    Main entrypoint for command line interface invoked with `pashehnet`
    :return: None
    """
    fire.Fire(Runner)


if __name__ == '__main__':
    cli_main()
