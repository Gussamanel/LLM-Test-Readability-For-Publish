import cmd as shell

class SetupCfgCommandConfig(NamedTuple):
    name: ClassVar[str]
    root_path: ClassVar[str]
    description: ClassVar[str]
    user_options: ClassVar[List[str]]
    commands: ClassVar[Tuple[str]]
    camel: ClassVar[str]

