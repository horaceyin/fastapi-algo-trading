from fastapi import APIRouter, Depends, status
from services.auth_service import AuthService
from schemas.auth_schemas import UserLogin, AccountSumModel

# Testing msg when this router is called
@staticmethod
def print_msg():
    print("Calling at login router.")

# Set up router
loginRouter = APIRouter(
    tags=['Authentication'],
    prefix='/login',
    dependencies=[Depends(print_msg)]
)

# Post method for login router
# Starting with host/login/
@loginRouter.post('/', status_code=status.HTTP_200_OK)
async def user_login(request: UserLogin):
    return AuthService.user_login(request)

# @loginRouter.post('/info', status_code=status.HTTP_200_OK)
# async def infomation(requset: UserInfo):
#     client = AuthService.user_login(request) # Output of userLogin # Will hold until data is retrived # Need await to do rest of code
#     print(client)
#     token = client['data']['sessionToken'] # Session token
#     targetacc = client['data']['userId']

#     secReq = {
#         'sessionToken': token,
#         'targetAccNo': targetacc
#     }
#     # info = await AuthService.acc_login(request= json.dumps(secReq)) # Turn secReq into json object, then pass as request
#     info = "Hello" # Testing code # Currently: Code 200, "string"
#     return info

@loginRouter.post('/info', status_code=status.HTTP_200_OK)
async def infomation(request: AccountSumModel):
    return AuthService.get_acc_info(request)
