import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = BASE_DIR # Currently files are in root, but could be moved to 'data' folder

# File names
JSON_FILENAME = 'steam_games.json'
CSV_FILENAME = 'steam_games.csv'

# Full paths
JSON_FILE_PATH = os.path.join(DATA_DIR, JSON_FILENAME)
CSV_FILE_PATH = os.path.join(DATA_DIR, CSV_FILENAME)

# App settings
APP_TITLE = 'Proyecto MLOPS'
APP_DESCRIPTION = 'Proyecto Machine Learning Operations'
APP_VERSION = '1.0.0'
