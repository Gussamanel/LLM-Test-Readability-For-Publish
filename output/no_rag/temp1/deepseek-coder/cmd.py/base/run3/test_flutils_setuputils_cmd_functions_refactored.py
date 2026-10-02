import pytest
import cmd as module_0

def test_command_class_build_with_valid_config_should_return_the_correct_command():
    # Constants
    COMMAND_NAME = "TestCommand"
    COMMAND_DESCRIPTION = "This is a test command."
    COMMAND_CAMEL = "Test"
    COMMAND_ROOT_PATH = ""
    COMMAND_COMMANDS = ("command1", "command2")
    SETUP_CFG_FILE_PATH = "./setup.cfg"

    # Setup
    setup_cfg = SetupCfgCommandConfig(
        name=COMMAND_NAME,
        description=COMMAND_DESCRIPTION,
        camel=COMMAND_CAMEL,
        root_path=COMMAND_ROOT_PATH,
        commands=COMMAND_COMMANDS
    )

    # Execution
    command_class = module_0.build_setup_cfg_command_class(setup_cfg)

    # Assertion
    assert command_class.name == COMMAND_NAME
    assert command_class.description == COMMAND_DESCRIPTION
    assert command_class.root_path == COMMAND_ROOT_PATH
    assert command_class.commands == COMMAND_COMMANDS

    # Additional assertions to check the type and module can be added here

