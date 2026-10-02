import cmd as cmd_module

def test_should_build_setup_cfg_command_class():
    NAME = 'SetupCfg'
    ROOT_PATH = ''
    DESCRIPTION = 'A description for the setup command class'
    USER_OPTIONS = []
    COMMANDS = ('command1', 'command2')

    setup_command_config = SetupCfgCommandConfig(
        name=NAME,
        root_path=ROOT_PATH,
        description=DESCRIPTION,
        user_options=USER_OPTIONS,
        commands=COMMANDS
    )

    setup_command_class = module_0.build_setup_cfg_command_class(setup_command_config)

    assert setup_command_class.name == NAME
    assert setup_command_class.root_path == ROOT_PATH
    assert setup_command_class.description == DESCRIPTION
    assert setup_command_class.user_options == USER_OPTIONS
    assert setup_command_class.commands == COMMANDS

