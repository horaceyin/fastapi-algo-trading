from os import environ, path, mkdir
from dotenv import load_dotenv

load_dotenv()
logdir = environ['LOG_DIRECTORY']
if not path.exists(logdir): mkdir(logdir)

from fastapi import FastAPI
import uvicorn
from core import config
from routers.authentication.login import loginRouter
from routers.dashboard.backtesting import backtestingRouter
from routers.dashboard.technical_analysis import taRouter

ROUTERSLIST = [
    loginRouter,
    backtestingRouter,
    taRouter
]

app = FastAPI()

for router in ROUTERSLIST:
    app.include_router(router)

@app.get('/')
async def root():
    return {'msg':'render main page'}

def create_log():
    logFile = environ['LOG_PATH']
    if not path.exists(logFile):
        log = open(logFile, 'w')
        log.close()

def get_config():
    if environ['ENV_STATE'] == 'dev':
        return config.DevConfig()
    return config.ProdConfig()

if __name__ == '__main__':
    create_log()
    myConfig = get_config()
    uvicorn.run('main:app', host = myConfig.HOST, port=myConfig.PORT, reload = True)