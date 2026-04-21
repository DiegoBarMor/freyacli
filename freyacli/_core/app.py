import os
from pathlib import Path
from abc import ABC, abstractmethod

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class App(ABC):
    _APP_NAME = "FreyacliApp" # override these values
    _VERSION = "0.1.0"

    # --------------------------------------------------------------------------
    def __init__(self, args: list[str], path_fyr: str|Path, path_fyh: str|Path):
        try:
            fy.WIDTH_TERMINAL, _ = os.get_terminal_size()
            if not fy.WIDTH_TERMINAL: fy.WIDTH_TERMINAL = 1
        except OSError:
            ### [NOTE] this can happen when e.g. using > in a shell
            #### In that case just use a default width value.
            fy.WIDTH_TERMINAL = 80
            fy.VALID_TERMINAL = False

        fy_parser = fy.FreyaParser.from_files(path_fyr, path_fyh)
        self.args = fy.ArgsParser(fy_parser, self._APP_NAME, self._VERSION)
        self.args.parse_args(args)


    # --------------------------------------------------------------------------
    @abstractmethod
    def run(self):
        """
        Override this method to implement the logic of the app.
        You can use the methods `get_path_to_root`, `arg_keys`, `get_arg_value` (and its), `set_arg_value`, to access the parsed arguments.
        """
        pass


    # --------------------------------------------------------------------------
    def get_path_to_root(self) -> list[str]:
        return self.args.get_path_to_root()


    # --------------------------------------------------------------------------
    def arg_keys(self) -> list[str]:
        return self.args.arg_keys()


    # --------------------------------------------------------------------------
    def get_arg_value(self, key: str, default = None):
        val = self.args.get_arg_value(key)
        if val is None: return default
        if isinstance(val, list) and not val: return default
        return val


    # --------------------------------------------------------------------------
    def set_arg_value(self, key: str, value):
        self.args.set_arg_value(key, value)


    # --------------------------------------------------------------------------
    def help_and_exit(self, exit_code: int, *err_messages: str):
        self.args.help_and_exit(exit_code, *err_messages)


    # --------------------------------------------------------------------------
    def assert_file_in(self, path: Path, allow_none: bool = False):
        err = fy.PathAssertion.file_in(path, allow_none)
        if isinstance(err, fy.ArgDTypeError):
            self.help_and_exit(1, err.err_message)


    # --------------------------------------------------------------------------
    def assert_file_out(self, path: Path, allow_none: bool = False):
        err = fy.PathAssertion.file_out(path, allow_none)
        if isinstance(err, fy.ArgDTypeError):
            self.help_and_exit(1, err.err_message)


    # --------------------------------------------------------------------------
    def assert_dir_out(self, path: Path, allow_none: bool = False):
        err = fy.PathAssertion.dir_out(path, allow_none)
        if isinstance(err, fy.ArgDTypeError):
            self.help_and_exit(1, err.err_message)


    # --------------------------------------------------------------------------
    def get_arg_bool(self, key: str, default = None) -> bool:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). Flags with no value attached always store a boolean value."""
        return self.get_arg_value(key, default)


    # --------------------------------------------------------------------------
    def get_arg_str(self, key: str, default = None) -> str:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        return self.get_arg_value(key, default)


    # --------------------------------------------------------------------------
    def get_arg_path(self, key: str, default = None) -> Path:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        return self.get_arg_value(key, default)


    # --------------------------------------------------------------------------
    def get_arg_int(self, key: str, default = None) -> int:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        return self.get_arg_value(key, default)


    # --------------------------------------------------------------------------
    def get_arg_float(self, key: str, default = None) -> float:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        return self.get_arg_value(key, default)


    # --------------------------------------------------------------------------
    def get_arg_list_str(self, key: str, default = None) -> list[str]:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        val = self.get_arg_value(key)
        if val is None: return default
        if isinstance(val, list): return val
        return [val]


    # --------------------------------------------------------------------------
    def get_arg_list_path(self, key: str, default = None) -> list[Path]:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        val = self.get_arg_value(key)
        if val is None: return default
        if isinstance(val, list): return val
        return [val]


    # --------------------------------------------------------------------------
    def get_arg_list_int(self, key: str, default = None) -> list[int]:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        val = self.get_arg_value(key)
        if val is None: return default
        if isinstance(val, list): return val
        return [val]


    # --------------------------------------------------------------------------
    def get_arg_list_float(self, key: str, default = None) -> list[float]:
        """This method is for helping with intended usage, **no asertion is performed** (value was already parsed/asserted earlier). When an optional positional value is absent, the actual stored value will be `None`.
        When an optional flag value is absent, the actual stored value will be `True` (since the flag was used, but no value was attached)."""
        val = self.get_arg_value(key)
        if val is None: return default
        if isinstance(val, list): return val
        return [val]


# //////////////////////////////////////////////////////////////////////////////
