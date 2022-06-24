from fastapi import FastAPI
from dotenv import dotenv_values
from pydantic import BaseModel, BaseSettings
import uvicorn
from core import config
from routers.authentication.login import loginRouter
from routers.dashboard.backtesting import backtestingRouter

DOTENV = '.env'
ROUTERSLIST = [
    loginRouter,
    backtestingRouter
]

def get_config():
    env = dotenv_values(DOTENV)
    if env['ENV_STATE'] == 'dev':
        return config.DevConfig()
    return config.ProdConfig()

app = FastAPI()

for router in ROUTERSLIST:
    app.include_router(router)

@app.get('/')
async def root():
    return {'msg':'render main page'}


if __name__ == '__main__':
    myConfig = get_config()
    uvicorn.run('main:app', host = myConfig.HOST, port=myConfig.PORT, reload = True)