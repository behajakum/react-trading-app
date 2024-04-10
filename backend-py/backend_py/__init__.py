# Initialise logger, env variables and dependant paths
import os
import sys
from dotenv import load_dotenv
import logging
from backend_py.utils.create_logger import create_logger

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

is_console_log = True if os.getenv('CONSOLE_LOG').lower() == 'true' else False
is_file_log = True if os.getenv('FILE_LOG').lower() == 'true' else False

create_logger(is_console=is_console_log, is_file=is_file_log)
logger = logging.getLogger(__name__)

logger.info(f"Logger initialised. console: {is_console_log}, file: {is_file_log}")
# logger.info(f'System Paths: {sys.path}')