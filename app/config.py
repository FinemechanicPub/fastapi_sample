from pydantic import BaseModel, Field, PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Db(BaseModel):
    scheme: str = "postgresql+asyncpg"
    host: str = "postgres"
    port: int = 5432
    user: str = "postgres"
    password: SecretStr = SecretStr("")

    @computed_field
    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password.get_secret_value(),
        )


class Api(BaseModel):
    page_size: int = Field(default=10, ge=1)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="_", env_nested_max_split=1
    )
    db: Db = Db()
    api: Api = Api()


settings = Settings()
