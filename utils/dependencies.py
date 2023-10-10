import models
import services
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database.unitofwork import UnitOfWork
from typing import Annotated

#services dependencies


UOWDependency = Annotated[UnitOfWork, Depends(UnitOfWork)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    # users_service: services.UsersService = Depends(get_users_services)
) -> models.User:
    return await services.users_service.get_current_user(token)




    
