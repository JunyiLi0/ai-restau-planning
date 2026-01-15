from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = ""

    # Application
    app_env: str = "development"
    debug: bool = True

    # File paths (relative to backend directory)
    upload_dir: str = "data/uploads"
    export_dir: str = "data/exports"
    template_dir: str = "data/templates"

    # Base directory
    base_dir: Path = Path(__file__).parent.parent.parent

    @property
    def upload_path(self) -> Path:
        return self.base_dir / self.upload_dir

    @property
    def export_path(self) -> Path:
        return self.base_dir / self.export_dir

    @property
    def template_path(self) -> Path:
        return self.base_dir / self.template_dir

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
