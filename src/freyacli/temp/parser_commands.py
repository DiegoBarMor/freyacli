# from collections import defaultdict

# # //////////////////////////////////////////////////////////////////////////////
# class PrismaTuiCliError(Exception):
#     """Custom exception for errors in the ParserCommands class.
#     Intended for catching bugs in code implementing prismatui.cli, not user errors."""
#     pass


# # //////////////////////////////////////////////////////////////////////////////
# class CLIError(Exception):
#     """Base class for CLI user-related errors."""
#     pass


# # //////////////////////////////////////////////////////////////////////////////
# class CLIArgument:
#     """Base class for CLI arguments."""
#     def __init__(self, name: str):
#         self.name = name
#         self.help_str = ''


#     # --------------------------------------------------------------------------
#     def add_help(self, help_str: str) -> "CLIArgument":
#         self.help_str = help_str
#         return self


# # //////////////////////////////////////////////////////////////////////////////
# class Posit(CLIArgument):
#     def __init__(self, name: str):
#         super().__init__(name)
#         self.idx: int = -1  # Position index, to be set when parsing

#     # --------------------------------------------------------------------------
#     def __repr__(self):
#         return f"Posit(name={self.name}, idx={self.idx})"


# # //////////////////////////////////////////////////////////////////////////////
# class Mode(Posit):
#     def __init__(self, name, alias: str):
#         super().__init__(name)
#         self.alias = alias

#     # --------------------------------------------------------------------------
#     def __repr__(self):
#         return f"Mode(name={self.name}, alias={self.alias}, idx={self.idx})"


# # //////////////////////////////////////////////////////////////////////////////
# class Flag(CLIArgument):
#     def __init__(self, name, *aliases: str):
#         super().__init__(name)
#         self.aliases = aliases

#         if len(aliases) == 0:
#             raise PrismaTuiCliError(f"Flag '{name}' must have at least one alias.")

#     # --------------------------------------------------------------------------
#     def __repr__(self):
#         return f"Flag(name={self.name}, aliases={self.aliases})"


# # //////////////////////////////////////////////////////////////////////////////
# class Kwarg(CLIArgument):
#     def __init__(self, name, *aliases: str):
#         super().__init__(name)
#         self.aliases = aliases

#         if len(aliases) == 0:
#             raise PrismaTuiCliError(f"Kwarg '{name}' must have at least one alias.")

#     # --------------------------------------------------------------------------
#     def __repr__(self):
#         return f"Kwarg(name={self.name}, aliases={self.aliases})"



# # //////////////////////////////////////////////////////////////////////////////
# class ParserCommands:
#     """
#     Class to manage the commands/flags/arguments provided to a CLI app.
#     For the purposes of this class, the CLI arguments are divided into 5 kinds.
#     When using the class, you can specify the arguments and which kinds they correspond to.

#     The kinds are:
#     - `namepy`: The name of the script being executed. Essentially sys.argv[0].
#         e.g. "python some_script.py" -> `namepy` is "some_script.py".
#     - `posits`: Analogous to positional arguments in python's functions, these are arguments
#         that come after `namepy` but before any `flags` or `kwargs`.
#         e.g. "python some_script.py arg1 arg2 --flag1 --kwarg1 val1" -> `posits` are ["arg1", "arg2"].
#     - `modes`: Special kind of `posits` that define the mode of operation for the script. They are mutually exclusive and usually come right after `namepy`.
#         e.g. "python some_script.py mode1 --flag1" -> `modes` is "mode1".
#     - `flags`: Boolean switches that modify the behavior of the script. They usually start with `--` or `-`,
#         but this is not enforced by `ParserCommands`.
#         e.g. "python some_script.py --verbose --debug" -> `flags` are ["verbose", "debug"].
#     - `kwargs`: Key-value pairs that provide additional information to the script. They usually start with `--` or `-`,
#         but this is not enforced by `ParserCommands`.
#         e.g. "python some_script.py --input data.csv --output result.txt" -> `kwargs` are {"input": "data.csv", "output": "result.txt"}.

#     Examples of diverse CLI commands in a real application:
#         - ```conda create --name prismatui -y```: `conda` is `namepy`, `create` is a `mode`, `--name` is a `kwarg` with value `prismatui`, and `-y` is a `flag`.
#         - ```conda activate prismatui```: `conda` is `namepy`, `activate` is a `mode`, and `prismatui` is a `posit`.
#     """


#     # --------------------------------------------------------------------------
#     def _safe_add_expected_posit(self, posit: Posit) -> None:
#         if posit.name in self._expected_posits:
#             raise PrismaTuiCliError(f"Duplicate Posit name '{posit.name}' in expected_cliargs.")
#         self._expected_posits[posit.name] = posit


#     # --------------------------------------------------------------------------
#     def _safe_add_expected_mode(self, mode: Mode) -> None:
#         sibling_modes = self._expected_modes.get(mode.name, {})
#         if mode.alias in sibling_modes:
#             raise PrismaTuiCliError(f"Duplicate Mode alias '{mode.alias}' with name '{mode.name}' in expected_cliargs.")
#         self._expected_modes[mode.name][mode.alias] = mode


#     # --------------------------------------------------------------------------
#     def _safe_add_expected_flag(self, flag: Flag) -> None:
#         if flag.name in self._expected_flags:
#             raise PrismaTuiCliError(f"Duplicate Flag name '{flag.name}' in expected_cliargs.")
#         self._expected_flags[flag.name] = flag

#         for alias in flag.aliases:
#             if alias in self._known_flag_aliases:
#                 raise PrismaTuiCliError(f"Duplicate Flag alias '{alias}' in expected_cliargs.")
#             self._known_flag_aliases.add(alias)


#     # --------------------------------------------------------------------------
#     def _safe_add_expected_kwarg(self, kwarg: Kwarg) -> None:
#         if kwarg.name in self._expected_kwargs:
#             raise PrismaTuiCliError(f"Duplicate Kwarg name '{kwarg.name}' in expected_cliargs.")
#         self._expected_kwargs[kwarg.name] = kwarg

#         for alias in kwarg.aliases:
#             if alias in self._known_kwarg_aliases:
#                 raise PrismaTuiCliError(f"Duplicate Kwarg alias '{alias}' in expected_cliargs.")
#             self._known_kwarg_aliases.add(alias)


#     # --------------------------------------------------------------------------
#     def __init__(self, *expected_cliargs: CLIArgument) -> None:
#         self.namepy: str = ""

#         self._expected_posits: dict[str, Posit] = {}
#         self._expected_modes: dict[str, dict[str, Mode]] = defaultdict(dict)
#         self._expected_flags: dict[str, Flag] = {}
#         self._expected_kwargs: dict[str, Kwarg] = {}

#         self._known_flag_aliases: set[str] = set()
#         self._known_kwarg_aliases: set[str] = set()

#         for arg in expected_cliargs:
#             match arg:
#                 case Mode():  self._safe_add_expected_mode(arg)
#                 case Posit(): self._safe_add_expected_posit(arg)
#                 case Flag():  self._safe_add_expected_flag(arg)
#                 case Kwarg(): self._safe_add_expected_kwarg(arg)


#     # --------------------------------------------------------------------------
#     def get_posit(self, name: str) -> Posit:
#         if name not in self._expected_posits:
#             raise PrismaTuiCliError(f"Unknown Posit '{name}'.")
#         return self._expected_posits[name]


#     # --------------------------------------------------------------------------
#     def get_mode(self, name: str, alias: str) -> Mode:
#         if name not in self._expected_modes:
#             raise PrismaTuiCliError(f"Unknown Mode '{name}'.")
#         if alias not in self._expected_modes[name]:
#             raise PrismaTuiCliError(
#                 f"Unknown Mode with alias '{alias}' for Modes '{name}'. "
#                 f"Known aliases are: {list(self._expected_modes[name].keys())}"
#             )
#         return self._expected_modes[name]


#     # --------------------------------------------------------------------------
#     def get_flag(self, name: str) -> Flag:
#         if name not in self._expected_flags:
#             raise PrismaTuiCliError(f"Unknown Flag '{name}'.")
#         return self._expected_flags[name]


#     # --------------------------------------------------------------------------
#     def get_kwarg(self, name: str) -> Kwarg:
#         if name not in self._expected_kwargs:
#             raise PrismaTuiCliError(f"Unkown Kwarg '{name}'.")
#         return self._expected_kwargs[name]


#     # --------------------------------------------------------------------------
#     def parse(self, argv: list[str]) -> None:

#         if len(argv) < 1:
#             raise CLIError("No arguments provided to parse.")

#         self.namepy = argv[0]




# # //////////////////////////////////////////////////////////////////////////////
