from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict




class DbSettings(BaseModel):
    alembic_url: str = f"postgresql+asyncpg://postgres:77girado@185.200.243.110:5433/postgres"
        


class Settings(BaseSettings):
    ADMIN_TG_IDS: list[int]
    BOT_TOKEN: str
    HOUR: str
    MINUTE: str

    MEDIA_URL: str
    DB_HOST: str
    DB_PORT:str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ECHO: bool

    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str


    PUBLISHED_STATUS_ID: int
    ARCHIVED_STATUS_ID: int
    NOT_FILLED_IN_STATUS_ID: int


    @property
    def DATABASE_URL(self): 
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    

    media_filename: str = "media"
    products_media_dir: str = "products/"
    blogs_media_dir: str = "blogs/"
    users_media_dir: str = "users/"
    dealers_media_dir: str = "dealers/"
    payment_methods_media_dir: str = "payment_methods/"
    logos_media_dir: str = "logos/"
    social_media_media_dir: str = "social_media/"
    contacts_media_dir: str = "contacts/"
    delivery_media_dir: str = "delivery/"
   

    @property
    def PRODUCT_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.products_media_dir}"
    
   
    @property
    def BLOG_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.blogs_media_dir}"
    
    @property
    def USER_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.users_media_dir}"
    
    @property
    def DEALER_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.dealers_media_dir}"

    @property
    def PAYMENT_METHOD_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.payment_methods_media_dir}"
    
    @property
    def LOGO_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.logos_media_dir}"
    
    @property
    def SOCIAL_MEDIA_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.social_media_media_dir}"

    @property
    def CONTACT_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.contacts_media_dir}"
    
    @property
    def DELIVERY_MEDIA_URL(self):
        return f"{settings.MEDIA_URL}{self.delivery_media_dir}"

    api_v1_prefix: str = "/v1"
    development: bool = False
    db: DbSettings = DbSettings()
    
    

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()



