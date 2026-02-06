"""Test script for ConfigManager."""

import os
from pathlib import Path

from src.utils.config import ConfigManager, DiagnosticRules


def test_config_loading():
    """Test ConfigManager loading from JSON config file."""
    print("Testing ConfigManager...")

    # Test 1: Load from .matlab-lsprc.json
    print("\n1. Testing loading from .matlab-lsprc.json...")
    config_mgr = ConfigManager()
    settings = config_mgr.load()

    print(f"   matlabPath: {settings.matlabPath}")
    print(f"   maxDiagnostics: {settings.maxDiagnostics}")
    print(f"   diagnosticRules.all: {settings.diagnosticRules.all}")
    print(f"   diagnosticRules.unusedVariable: {settings.diagnosticRules.unusedVariable}")
    print(f"   formatting.indentSize: {settings.formatting.indentSize}")
    print(f"   completion.enableSnippets: {settings.completion.enableSnippets}")
    print(f"   cache.enabled: {settings.cache.enabled}")

    # Verify values match config file
    assert settings.maxDiagnostics == 100, "maxDiagnostics should be 100"
    assert settings.diagnosticRules.all is True, "diagnosticRules.all should be True"
    assert settings.formatting.indentSize == 4, "indentSize should be 4"
    assert settings.completion.maxSuggestions == 50, "maxSuggestions should be 50"
    assert settings.cache.enabled is True, "cache.enabled should be True"
    print("   [OK] JSON config loading successful!")

    # Test 2: Test convenience methods
    print("\n2. Testing convenience methods...")
    print(f"   get_matlab_path(): {config_mgr.get_matlab_path()}")
    print(f"   get_max_diagnostics(): {config_mgr.get_max_diagnostics()}")
    print(f"   get_diagnostic_rules(): {config_mgr.get_diagnostic_rules()}")
    print(f"   get_formatting_config(): {config_mgr.get_formatting_config()}")
    print(f"   get_completion_config(): {config_mgr.get_completion_config()}")
    print(f"   get_cache_config(): {config_mgr.get_cache_config()}")
    print("   [OK] Convenience methods work!")

    # Test 3: Test environment variable override
    print("\n3. Testing environment variable override...")
    os.environ['MATLAB_LSP_MAXDIAGNOSTICS'] = '250'
    config_mgr_env = ConfigManager()
    settings_env = config_mgr_env.load()
    print(f"   MATLAB_LSP_MAXDIAGNOSTICS set to '250'")
    print(f"   maxDiagnostics from config: {settings_env.maxDiagnostics}")
    assert settings_env.maxDiagnostics == 250, "Environment variable should override JSON config"
    print("   [OK] Environment variable override successful!")
    del os.environ['MATLAB_LSP_MAXDIAGNOSTICS']

    # Test 4: Test default values
    print("\n4. Testing default values...")
    config_mgr_default = ConfigManager()
    settings_default = config_mgr_default.load()
    # Remove config file temporarily to test defaults
    config_path = Path.cwd() / '.matlab-lsprc.json'
    config_backup = config_path.read_text() if config_path.exists() else None
    if config_path.exists():
        config_path.rename(config_path.with_suffix('.json.bak'))

    try:
        config_mgr_no_file = ConfigManager()
        settings_no_file = config_mgr_no_file.load()
        print(f"   matlabPath (no file): '{settings_no_file.matlabPath}'")
        print(f"   maxDiagnostics (no file): {settings_no_file.maxDiagnostics}")
        assert settings_no_file.matlabPath == "", "matlabPath should default to empty string"
        assert settings_no_file.maxDiagnostics == 100, "maxDiagnostics should default to 100"
        print("   [OK] Default values work!")
    finally:
        # Restore config file
        if config_backup:
            config_path.with_suffix('.json.bak').write_text(config_backup)
            config_path.with_suffix('.json.bak').replace(config_path)

    # Test 5: Test validation
    print("\n5. Testing validation...")
    try:
        from src.utils.config import MatlabLspSettings
        # This should raise ValueError if path doesn't exist
        invalid_settings = MatlabLspSettings(matlabPath="/nonexistent/path")
        print("   [FAIL] Validation should have raised ValueError for non-existent path")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   [OK] Validation correctly raised ValueError: {e}")

    print("\n[OK] All ConfigManager tests passed!")
    return True


if __name__ == "__main__":
    test_config_loading()
