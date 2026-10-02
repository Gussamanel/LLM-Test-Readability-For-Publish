import cmd as cmd_module

def test_command_class_builder():
    """
    Test the `build_setup_cfg_command_class` function.
    Here we test that `build_setup_cfg_command_class` correctly builds a command class with the correct attributes from the provided config.
    """
    # Setup
    setup_command_cfg = SetupCfgCommandConfig(
        name='test_command',
        description='A test command',
        commands=('test_command1', 'test_command2')
    )

    # Execution
    built_command_class = module_0.build_setup_cfg_command_class(setup_command_cfg)

    # Assertion
    assert built_command_class.name == setup_command_cfg.name
    assert built_command_class.root_path == ''
    assert built_command_class.description == setup_command_cfg.description
    assert built_command_class.commands == setup_command_cfg.commands

