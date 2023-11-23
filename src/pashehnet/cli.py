import logging
import os
import sys

import fire
from envyaml import EnvYAML

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


class Runner(object):
    """
    Provides a wrapper to create the network and kick off the simulation from
    a command line interface
    """
    DEFAULT_CONFIG_FNAME = './config.yaml'
    CURRENT_CONFIG_VERSION = 1

    def run(self, config_fname=DEFAULT_CONFIG_FNAME):
        """
        Create and run the network simulation
        :param config_fname: Network configuration filename
        :return: None
        """
        logging.debug('Starting runner')
        try:
            config = self._load_config(config_fname)  # noqa: F841
        except AssertionError as e:
            logging.error(e)

    def check(self, config_fname=DEFAULT_CONFIG_FNAME):
        """
        Load and validate network configuration, without creating or running it
        :param config_fname: Network configuration filename
        :return: None
        """
        logging.debug('Starting configuration check')
        try:
            config = self._load_config(config_fname)  # noqa: F841
        except AssertionError as e:
            logging.error(e)

    @staticmethod
    def _load_config(config_fname):
        """
        Load and validate the given configuration filename
        :param config_fname: Network configuration filename
        :return: Loaded config
        """
        logging.debug(f'Loading configuration file: {config_fname}')
        config = EnvYAML(config_fname)
        Runner._validate_config(config)
        return config

    @staticmethod
    def _validate_config(config):
        """
        Validate the provided configuration
        :param config: Loaded configuration
        :return: None
        """
        logging.debug('Validating configuration')
        assert Runner.CURRENT_CONFIG_VERSION == config['version'], \
            f'Expected config version to be {Runner.CURRENT_CONFIG_VERSION}, got {config["version"]}'  # noqa: E501
        # TODO Add additional validation of required config file flags


def cli_main():
    runner = Runner()
    fire.Fire(runner)
