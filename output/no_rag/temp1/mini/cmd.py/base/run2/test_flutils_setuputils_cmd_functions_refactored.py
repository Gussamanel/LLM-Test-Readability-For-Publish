import pytest

import cmd as cmd_module

def test_build_setup_cfg_command_class_raises_when_config_is_none():
    # Ensure the function fails fast when given a missing/None configuration.
    # The implementation accesses attributes on the config, so passing None should raise AttributeError.
    EXPECTED_EXCEPTION = AttributeError
    missing_setup_cfg = None  # Simulates a missing SetupCfgCommandConfig

    with pytest.raises(EXPECTED_EXCEPTION):
        module_0.build_setup_cfg_command_class(missing_setup_cfg)

