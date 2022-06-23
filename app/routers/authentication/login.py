from fastapi import APIRouter, Depends, status
from services.auth_service import AuthService
from schemas.auth_schemas import UserLogin

@staticmethod
def print_msg():
    print("Calling at login router.")

loginRouter = APIRouter(
    tags=['authentication'],
    prefix='/login',
    dependencies=[Depends(print_msg)]
)

@loginRouter.post('/', status_code=status.HTTP_200_OK)
async def user_login(request: UserLogin):
    return AuthService.user_login(request)
