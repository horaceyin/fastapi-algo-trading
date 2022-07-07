from os import path, mkdir
from core import config

# create logs folder if it doesn't exists in the first run
logdir = config.ENV_FILE['LOG_DIRECTORY']
if not path.exists(logdir): mkdir(logdir)

from fastapi import FastAPI
import uvicorn
from core.routers_list import ROUTERS_LIST

app = FastAPI()

# set up routers list
for router in ROUTERS_LIST:
    app.include_router(router)

@app.get('/')
async def root():
    return {'msg':'render main page'}

# create fastapi_logging.log inside logs folder
def create_log():
    logFile = config.ENV_FILE['LOG_PATH']
    if not path.exists(logFile):
        log = open(logFile, 'w')
        log.close()

# return configuration for production environment
def get_config():
    if config.ENV_FILE['ENV_STATE'] == 'dev':
        return config.DevConfig()
    return config.ProdConfig()

# starting point
if __name__ == '__main__':
    create_log()
    myConfig = get_config()
    # 'main:app' means FastAPI object called app under main.py
    uvicorn.run('main:app', host = myConfig.HOST, port=myConfig.PORT, reload = True)