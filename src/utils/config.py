"""Configuration management for MATLAB LSP Server."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class DiagnosticRules(BaseModel):
    """Diagnostic rules configuration."""

    all: bool = True
    unusedVariable: bool = True
    missingSemicolon: bool = False


class FormattingConfig(BaseModel):
    """Code formatting configuration."""

    indentSize: int = 4
    insertSpaces: bool = True


class CompletionConfig(BaseModel):
    """Code completion configuration."""

    enableSnippets: bool = True
    maxSuggestions: int = 50


class CacheConfig(BaseModel):
    """Cache configuration."""

    enabled: bool = True
    maxSize: int = 1000


class JsonConfigSettingsSource(PydanticBaseSettingsSource):
    """Custom settings source that loads variables from .matlab-lsprc.json."""

    def __init__(self, settings_cls: type[BaseSettings]):
        super().__init__(settings_cls)
        self.config_file_path: Path = Path.cwd() / '.matlab-lsprc.json'

    def get_field_value(
        self,
        field_name: str,
        field: Any,
    ) -> tuple[Any, str, bool]:
        """Get field value from JSON config file."""
        if not self.config_file_path.exists():
            return None, field_name, False

        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None, field_name, False

        # Handle nested configuration
        field_value = None
        for key in ['diagnosticRules', 'formatting', 'completion', 'cache']:
            if key in config_data and field_name in config_data[key]:
                field_value = config_data[key][field_name]
                break

        if field_value is None and field_name in config_data:
            field_value = config_data[field_name]

        return field_value, field_name, False

    def prepare_field_value(
        self,
        field_name: str,
        field: Any,
        value: Any,
        value_is_complex: bool,
    ) -> Any:
        """Prepare field value for pydantic."""
        return value

    def __call__(self) -> dict[str, Any]:
        """Return configuration dictionary."""
        config_dict: dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field,
                field_name,
            )
            field_value = self.prepare_field_value(
                field_name,
                field,
                field_value,
                value_is_complex,
            )
            if field_value is not None:
                config_dict[field_key] = field_value

        return config_dict


class MatlabLspSettings(BaseSettings):
    """MATLAB LSP Server settings."""

    matlabPath: str = Field(
        default="",
        description="Path to MATLAB installation directory"
    )
    maxDiagnostics: int = Field(
        default=100,
        ge=0,
        le=1000,
        description="Maximum number of diagnostics to report"
    )
    diagnosticRules: DiagnosticRules = Field(
        default_factory=DiagnosticRules,
        description="Diagnostic rules configuration"
    )
    formatting: FormattingConfig = Field(
        default_factory=FormattingConfig,
        description="Code formatting configuration"
    )
    completion: CompletionConfig = Field(
        default_factory=CompletionConfig,
        description="Code completion configuration"
    )
    cache: CacheConfig = Field(
        default_factory=CacheConfig,
        description="Cache configuration"
    )

    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        env_prefix='MATLAB_LSP_',
        case_sensitive=False,
    )

    @field_validator('matlabPath', mode='after')
    @classmethod
    def validate_matlab_path(cls, v: str) -> str:
        """Validate MATLAB path exists."""
        if v and not Path(v).exists():
            raise ValueError(f'MATLAB path does not exist: {v}')
        return v

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources to include JSON config file."""
        return (
            init_settings,
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


class ConfigManager:
    """Manager for LSP server configuration."""

    def __init__(self, config_file: Path | None = None):
        """Initialize ConfigManager.

        Args:
            config_file: Path to .matlab-lsprc.json file
        """
        self._settings: MatlabLspSettings | None = None
        self._config_file = config_file

    def load(self) -> MatlabLspSettings:
        """Load configuration from file and environment variables.

        Returns:
            Loaded configuration settings
        """
        if self._settings is None:
            self._settings = MatlabLspSettings()
        return self._settings

    @property
    def settings(self) -> MatlabLspSettings:
        """Get loaded settings.

        Returns:
            Configuration settings (loads if not already loaded)
        """
        if self._settings is None:
            self._settings = self.load()
        return self._settings

    def get_matlab_path(self) -> str:
        """Get MATLAB installation path.

        Returns:
            Path to MATLAB directory
        """
        return self.settings.matlabPath

    def get_max_diagnostics(self) -> int:
        """Get maximum number of diagnostics.

        Returns:
            Maximum diagnostics count
        """
        return self.settings.maxDiagnostics

    def get_diagnostic_rules(self) -> DiagnosticRules:
        """Get diagnostic rules configuration.

        Returns:
            Diagnostic rules
        """
        return self.settings.diagnosticRules

    def get_formatting_config(self) -> FormattingConfig:
        """Get formatting configuration.

        Returns:
            Formatting settings
        """
        return self.settings.formatting

    def get_completion_config(self) -> CompletionConfig:
        """Get completion configuration.

        Returns:
            Completion settings
        """
        return self.settings.completion

    def get_cache_config(self) -> CacheConfig:
        """Get cache configuration.

        Returns:
            Cache settings
        """
        return self.settings.cache
