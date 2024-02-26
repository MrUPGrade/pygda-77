import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_name: str
    db_port: int
    db_driver: str
    api_port: int

    model_config = SettingsConfigDict(env_prefix='pygda_')

    def get_db_url(self):
        return f'{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}'


settings = Settings()

# Test loading
if __name__ == '__main__':
    print(settings)