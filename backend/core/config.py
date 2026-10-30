from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PawFinder API"
    VERSION: str = "1.0.0"
    
    # Base de datos local
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Supabase (Auth y Storage) - Se usarán a partir de la Fase 3
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Lee las variables del archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()