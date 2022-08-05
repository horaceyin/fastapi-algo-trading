from pathlib import Path

APP_BASE_PATH = Path(__file__).parent.parent # Get the path for app folder #c:/Users/SP/Desktop/project/fastapi-algo-trading/app

TEMPLATES_PATH = APP_BASE_PATH.joinpath('templates') # c:\Users\SP\Desktop\project\fastapi-algo-trading\app\templates
STATIC_PATH = APP_BASE_PATH.joinpath('static') # c:\Users\SP\Desktop\project\fastapi-algo-trading\app\static