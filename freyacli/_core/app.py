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
        fy.WIDTH_TERMINAL, _ = os.get_terminal_size()
        if not fy.WIDTH_TERMINAL: fy.WIDTH_TERMINAL = 1

        fy_parser = fy.FreyaParser.from_files(path_fyr, path_fyh)
        self.args = fy.ArgsParser(fy_parser, self._APP_NAME, self._VERSION)
        self.args.parse_args(args)


    # --------------------------------------------------------------------------
    @abstractmethod
    def run(self):
        """
        Override this method to implement the logic of the app.
        You can use the methods `get_path_to_root`, `arg_keys`, `get_arg_value` (and its), `set_arg_value`, `assert_paths` to access the parsed arguments.
        """
        pass


    # --------------------------------------------------------------------------
    def get_path_to_root(self) -> list[str]:
        return self.args.get_path_to_root()


    # --------------------------------------------------------------------------
    def arg_keys(self) -> list[str]:
        return self.args.arg_keys()


    # --------------------------------------------------------------------------
    def get_arg_value(self, key: str):
        return self.args.get_arg_value(key)


    # --------------------------------------------------------------------------
    def get_arg_bool(self, key: str) -> bool:
        return fy.ArgDType.assert_type( self.get_arg_value(key), bool )

    def get_arg_str(self, key: str) -> str:
        return fy.ArgDType.assert_type( self.get_arg_value(key), str )

    def get_arg_path(self, key: str) -> Path:
        return fy.ArgDType.assert_type( self.get_arg_value(key), Path )

    def get_arg_int(self, key: str) -> int:
        return fy.ArgDType.assert_type( self.get_arg_value(key), int )

    def get_arg_float(self, key: str) -> float:
        return fy.ArgDType.assert_type( self.get_arg_value(key), float )


    # --------------------------------------------------------------------------
    def get_arg_list_bool(self, key: str) -> list[bool]:
        return fy.ArgDType.assert_type( self.get_arg_value(key), bool, list_expected = True )

    def get_arg_list_str(self, key: str) -> list[str]:
        return fy.ArgDType.assert_type( self.get_arg_value(key), str, list_expected = True )

    def get_arg_list_path(self, key: str) -> list[Path]:
        return fy.ArgDType.assert_type( self.get_arg_value(key), Path, list_expected = True )

    def get_arg_list_int(self, key: str) -> list[int]:
        return fy.ArgDType.assert_type( self.get_arg_value(key), int, list_expected = True )

    def get_arg_list_float(self, key: str) -> list[float]:
        return fy.ArgDType.assert_type( self.get_arg_value(key), float, list_expected = True )


    # --------------------------------------------------------------------------
    def set_arg_value(self, key: str, value):
        self.args.set_arg_value(key, value)


    # --------------------------------------------------------------------------
    def help_and_exit(self, exit_code: int, *err_messages: str):
        self.args.help_and_exit(exit_code, *err_messages)


    # --------------------------------------------------------------------------
    def assert_paths(self,
        keys_file_in:  list[str] = None,
        keys_file_out: list[str] = None,
        keys_dir_out:  list[str] = None,
    ) -> None:
        known_keys = set(self.arg_keys())

        def assertion(keys: list[str], assertion_func: callable) -> list[fy.ArgDTypeError]:
            if keys is None: return []
            vals = (
                self.get_arg_value(key) for key in keys
                if key in known_keys
            )
            return list(filter(
                lambda v: isinstance(v, fy.ArgDTypeError),
                map(assertion_func, vals)
            ))

        errors = [ err.err_message for err in \
            assertion(keys_file_in, fy.PathAssertion.file_in) + \
            assertion(keys_file_out, fy.PathAssertion.file_out) + \
            assertion(keys_dir_out, fy.PathAssertion.dir_out)
        ]
        if not errors: return

        self.help_and_exit(1, *errors)


# //////////////////////////////////////////////////////////////////////////////
