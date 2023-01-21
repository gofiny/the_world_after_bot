import logging.config

import yaml


def init_logger(config_file: str):
    with open(config_file, "r") as _file:
        config = yaml.load(_file, yaml.FullLoader)
    logging.config.dictConfig(config)
