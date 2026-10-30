from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PawFinder API"
    VERSION: str = "1.0.0"
    
    # Base de datos local
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Supabase (Auth y Storage)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""  # Agregamos esta línea

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()