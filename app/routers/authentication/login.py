from fastapi import APIRouter, Depends, status
from services.auth_service import AuthService
from schemas.auth_schemas import UserLogin
import json

@staticmethod
def print_msg():
    print("Calling at login router.")

loginRouter = APIRouter(
    tags=['Authentication'],
    prefix='/login',
    dependencies=[Depends(print_msg)]
)

@loginRouter.post('/', status_code=status.HTTP_200_OK)
async def user_login(request: UserLogin):
    
    client = await AuthService.user_login(request) # Output of userLogin # Will hold until data is retrived
    print(client)
    token = client['data']['sessionToken'] # Session token
    targetacc = client['data']['userId']

    secReq = {
        'sessionToken': token,
        'targetAccNo': targetacc
    }
    # info = await AuthService.acc_login(request= json.dumps(secReq)) # Turn secReq into json object, then pass as request
    info = "Hello" # Testing code
    return info
