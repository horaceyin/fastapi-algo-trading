from pathlib import Path

APP_BASE_PATH = Path(__file__).parent.parent

TEMPLATES_PATH = APP_BASE_PATH.joinpath('templates')
STATIC_PATH = APP_BASE_PATH.joinpath('static')