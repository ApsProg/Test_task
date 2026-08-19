from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    db_url : str

    jwt_jwks_url: str

    log_level : str = "INFO"

    service_machine: str = "callbacks-service"

    bootstrap_servers : str = "localhost:9092"

    producer_topic : str = "leads.events.v1"

    consumer_topic : str = "lead_moderation.evetns.v1"

    consumer_group_id : str = "moderation_event_consumer"


settings = Settings()
