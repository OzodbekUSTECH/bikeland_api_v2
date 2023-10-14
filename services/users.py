from schemas.users import CreateUserSchema, UpdateUserSchema,  TokenSchema
from security.password_handler import PasswordHandler
from datetime import timedelta
from schemas.users import TokenData
import models
from security.jwt_handler import JWTHandler
from database import UnitOfWork
from utils.exceptions import CustomException
from utils.media_handler import MediaHandler

from jose import JWTError

class UsersService:

    def __init__(self):
        self.uow = UnitOfWork()

    
    async def create_user(self, user_data: CreateUserSchema) -> models.User:
        user_dict = user_data.model_dump()
        hashed_password = PasswordHandler.hash(user_data.password)
        user_dict["password"] = hashed_password
        if user_data.filename is not None:
            filename = await MediaHandler.save_media(user_data.filename, MediaHandler.users_media_dir)
            user_dict["filename"] = filename
        async with self.uow:
            user = await self.uow.users.create(user_dict)
            await self.uow.commit()
            return user
        
    async def get_list_of_users(self) -> list[models.User]:
        async with self.uow:
            return await self.uow.users.get_all()
        
    async def get_user_by_id(self, id: int) -> models.User:
        async with self.uow:
            return await self.uow.users.get_by_id(id)
    
    async def update_user(self, id: int, user_data: UpdateUserSchema) -> models.User:
        async with self.uow:
            user: models.User = await self.uow.users.get_by_id(id)
            user_dict= user_data.model_dump(exclude={"filename"})
            if user_data.filename:
                filename = await MediaHandler.save_media(user_data.filename, MediaHandler.users_media_dir)
                user_dict["filename"] = filename

            await self.uow.users.update(user.id, user_dict)
            await self.uow.commit()
            return user
        
    async def delete_user(self, id: int) -> models.User:
        async with self.uow:
            user: models.User = await self.uow.users.get_by_id(id)
            await self.uow.users.delete(user.id)
            await self.uow.commit()
            return user

    ################################
    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        async with self.uow:
            user: models.User = await self.uow.users.get_by_email(email)
                
            if not user or not PasswordHandler.verify(password, user.password):
                raise CustomException.unauthorized("Incorrect email or password")

            access_token_expires = timedelta(minutes=JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES)

            access_token = await JWTHandler.create_access_token(
                data={"email": user.email}, expires_delta=access_token_expires
            )
            return TokenSchema(access_token=access_token, token_type="Bearer")
    
    async def get_current_user(self, token: str) -> models.User:
        credentials_exception = CustomException.unauthorized("Could not validate credentials")
        try:
            payload = await JWTHandler.decode(token)
            email: str = payload.get("email") 
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        
        async with self.uow:
        
            user = await self.uow.users.get_by_email(token_data.email)
            
            if user is None:
                raise credentials_exception

            return user
        

users_service = UsersService()