from fastapi import FastAPI
from dotenv import dotenv_values
from pydantic import BaseModel, BaseSettings
import uvicorn
from core import config
from routers.authentication import login

DOTENV = '.env'

app = FastAPI()

app.include_router(login.loginRouter)

@app.get('/')
async def root():
    return {'msg':'render main page'}

def get_config():
    env = dotenv_values(DOTENV)
    if env['ENV_STATE'] == 'dev':
        return config.DevConfig()
    return config.ProdConfig()

if __name__ == '__main__':
    myConfig = get_config()
    uvicorn.run('main:app', host = myConfig.HOST, port=myConfig.PORT, reload = True)