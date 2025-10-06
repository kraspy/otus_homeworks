from pathlib import Path

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parent


class DbConfig(BaseModel):
    driver_sync: str = 'postgresql'
    host: str = ''
    port: int = ''
    database: str = ''
    username: str = ''
    password: SecretStr = ''
    # ---
    echo: bool = True

    @property
    def sync_url(self):
        url = URL.create(
            drivername=self.driver_sync,
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
        )
        return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='APP__',
        env_nested_delimiter='__',
        env_file=(
            BASE_DIR / '.env',
            BASE_DIR / '.env.default',
        ),
    )
    db: DbConfig = DbConfig()


settings = Settings()

url = settings.db.sync_url.render_as_string(
    hide_password=False,
)
