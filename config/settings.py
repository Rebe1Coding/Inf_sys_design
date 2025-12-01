from pydantic_settings import BaseSettings


class Settings(BaseSettings):

        USER:str
        PASSWORD:str
        HOST:str
        PORT:str
        DATABASE:str
        POOL_MODE:str
        
        class Config:
            env_file =".env"





settings = Settings()