"""Configuration management for MATLAB LSP Server."""

import json
import os
import platform
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator
from pydantic.fields import FieldInfo
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
        self.config_file_path: Path = Path.cwd() / ".matlab-lsprc.json"

    def get_field_value(
        self,
        field: FieldInfo,
        field_name: str,
    ) -> tuple[Any, str, bool]:
        """Get field value from JSON config file."""
        if not self.config_file_path.exists():
            return None, field_name, False

        try:
            with open(self.config_file_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None, field_name, False

        # Handle nested configuration
        field_value = None
        for key in ["diagnosticRules", "formatting", "completion", "cache"]:
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
        default="", description="Path to MATLAB installation directory"
    )
    maxDiagnostics: int = Field(
        default=100,
        ge=0,
        le=1000,
        description="Maximum number of diagnostics to report",
    )
    diagnosticRules: DiagnosticRules = Field(
        default_factory=DiagnosticRules,
        description="Diagnostic rules configuration",
    )
    formatting: FormattingConfig = Field(
        default_factory=FormattingConfig,
        description="Code formatting configuration",
    )
    completion: CompletionConfig = Field(
        default_factory=CompletionConfig,
        description="Code completion configuration",
    )
    cache: CacheConfig = Field(
        default_factory=CacheConfig, description="Cache configuration"
    )

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_prefix="MATLAB_LSP_",
        case_sensitive=False,
    )

    @field_validator("matlabPath", mode="after")
    @classmethod
    def validate_matlab_path(cls, v: str) -> str:
        """Validate MATLAB path exists."""
        if v and not Path(v).exists():
            raise ValueError(f"MATLAB path does not exist: {v}")
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


def create_default_config(config_path: Path | None = None) -> Path:
    """Create default .matlab-lsprc.json configuration file.

    Args:
        config_path: Path where to create config file (default: CWD/.matlab-lsprc.json)

    Returns:
        Path to created config file
    """
    if config_path is None:
        config_path = Path.cwd() / ".matlab-lsprc.json"

    if config_path.exists():
        return config_path

    # Try to find MATLAB automatically
    matlab_path = _find_matlab_path()

    default_config = {
        "matlabPath": matlab_path if matlab_path else "",
        "maxDiagnostics": 100,
        "diagnosticRules": {
            "all": True,
            "unusedVariable": True,
            "missingSemicolon": False,
        },
        "formatting": {"indentSize": 4, "insertSpaces": True},
        "completion": {"enableSnippets": True, "maxSuggestions": 50},
        "cache": {"enabled": True, "maxSize": 1000},
    }

    config_path.write_text(
        json.dumps(default_config, indent=2), encoding="utf-8"
    )
    return config_path


def _find_matlab_path() -> Optional[str]:
    """Find MATLAB installation directory.

    Searches in multiple locations:
    1. System PATH (recursive search)
    2. Common MATLAB installation paths

    Returns:
        Path to MATLAB directory (e.g., "C:/Program Files/MATLAB/R2023b")
        or None if not found
    """
    # Search in PATH first
    matlab_path = _find_matlab_in_path()
    if matlab_path:
        return matlab_path

    # Search in common installation paths
    matlab_path = _find_matlab_in_common_paths()
    if matlab_path:
        return matlab_path

    return None


def _find_matlab_in_path() -> Optional[str]:
    """Recursively search for MATLAB in system PATH.

    Returns:
        Path to MATLAB directory or None
    """
    mlint_in_path = _find_mlint_in_path_recursive()
    if mlint_in_path:
        # mlint path: H:/MATLAB/R2023b/bin/win64/mlint.exe
        # Extract MATLAB path: H:/MATLAB/R2023b
        mlint_path = Path(mlint_in_path)

        # Navigate up 3 levels: win64 -> bin -> R2023b
        # This gives us the MATLAB version directory
        matlab_root = mlint_path
        for _ in range(3):
            matlab_root = matlab_root.parent
            if matlab_root.parent == matlab_root:
                return str(mlint_path.parent.parent)  # Fallback

        # Verify this looks like a MATLAB directory
        if "MATLAB" in str(matlab_root.parent) or (
            matlab_root.name.startswith("R") and len(matlab_root.name) == 5
        ):
            return str(matlab_root)

    return None


def _find_mlint_in_path_recursive() -> Optional[str]:
    """Recursively search for mlint.exe in PATH directories.

    Returns:
        Path to mlint.exe or None
    """
    mlint_names = ["mlint.exe", "mlint"] if platform.system() != "Windows" else ["mlint.exe", "mlint.bat"]

    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        base_dir = Path(path_dir)
        if not base_dir.exists():
            continue

        # Search recursively up to 3 levels deep
        for root, dirs, files in os.walk(base_dir):
            # Limit depth to avoid searching entire filesystem
            depth = root.replace(str(base_dir), "").count(os.sep)
            if depth > 3:
                dirs[:] = []  # Don't go deeper
                continue

            for mlint_name in mlint_names:
                if mlint_name in files:
                    full_path = Path(root) / mlint_name
                    if full_path.exists():
                        return str(full_path)

    return None


def _find_matlab_in_common_paths() -> Optional[str]:
    """Search for MATLAB in common installation paths.

    Returns:
        Path to MATLAB directory or None
    """
    # Common installation paths by platform
    if platform.system() == "Windows":
        common_paths = [
            Path("C:/Program Files/MATLAB"),
            Path("C:/Program Files (x86)/MATLAB"),
            Path("D:/Program Files/MATLAB"),
            Path("E:/Program Files/MATLAB"),
            Path("F:/Program Files/MATLAB"),
            Path("G:/Program Files/MATLAB"),
            Path("H:/Program Files/MATLAB"),
            Path("I:/Program Files/MATLAB"),
            Path("J:/Program Files/MATLAB"),
        ]
    elif platform.system() == "Darwin":  # macOS
        common_paths = [
            Path("/Applications/MATLAB_R*.app"),
            Path("/Applications/MATLAB.app"),
            Path("/usr/local/MATLAB"),
        ]
    else:  # Linux and others
        common_paths = [
            Path("/usr/local/MATLAB"),
            Path("/opt/MATLAB"),
            Path("/opt/matlab"),
            Path("/usr/local/matlab"),
            Path.home() / "MATLAB",
            Path.home() / "matlab",
            Path("/usr/share/matlab"),
        ]

    import glob as glob_module

    for base in common_paths:
        # Handle glob patterns (for version directories)
        if "*" in str(base):
            matches = glob_module.glob(str(base))
            for match in sorted(matches, reverse=True):
                # Try newest version first
                mlint_path = _find_mlint_in_dir(Path(match))
                if mlint_path:
                    return str(Path(match))
        elif base.exists():
            mlint_path = _find_mlint_in_dir(base)
            if mlint_path:
                return str(base)

    return None


def _find_mlint_in_dir(base_dir: Path) -> Optional[str]:
    """Find mlint in a directory tree.

    Args:
        base_dir: Base directory to search

    Returns:
        Path to mlint executable or None
    """
    # Platform-specific mlint binary names
    if platform.system() == "Windows":
        mlint_names = ["mlint.exe", "mlint.bat"]
    else:
        mlint_names = ["mlint"]

    # Search in bin directories first (faster)
    for root, dirs, files in os.walk(base_dir):
        if "bin" in root:
            for mlint_name in mlint_names:
                if mlint_name in files:
                    return str(Path(root) / mlint_name)

    # If not found in bin, search all directories (fallback)
    for root, dirs, files in os.walk(base_dir):
        for mlint_name in mlint_names:
            if mlint_name in files:
                return str(Path(root) / mlint_name)

    return None


def ensure_config_exists(
    config_path: Path | None = None, silent: bool = False
) -> bool:
    """Ensure configuration file exists, create default if missing.

    Args:
        config_path: Path to config file (default: CWD/.matlab-lsprc.json)
        silent: If True, don't log messages

    Returns:
        True if config was created, False if already existed
    """
    if config_path is None:
        config_path = Path.cwd() / ".matlab-lsprc.json"

    if config_path.exists():
        return False

    create_default_config(config_path)
    return True
