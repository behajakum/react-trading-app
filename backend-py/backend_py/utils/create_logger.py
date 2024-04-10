import os
import logging
import logging.config
import yaml

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def create_logger(is_console=True, is_file=False):
    with open(os.path.join(APP_DIR, 'config', 'logging.yaml'), 'r') as fh:
        config = yaml.safe_load(fh.read())
    log_file_dir = os.path.join(APP_DIR, 'logs')
    os.makedirs(log_file_dir, exist_ok=True)
    config['handlers']['file']['filename'] = os.path.join(log_file_dir, config["handlers"]["file"]["filename"])
    if is_console is False:
        config['root']['handlers'].remove('console')
        del config['handlers']['console']
    if is_file is False:
        config['root']['handlers'].remove('file')
        del config['handlers']['file']
    logging.config.dictConfig(config)


if __name__ == '__main__':
    create_logger(is_console=False, is_file=True)
    logger = logging.getLogger(__name__)
    logger.info(f'logger initialised')
