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
        """
        pass


    # --------------------------------------------------------------------------
    def get_path_to_root(self) -> list[str]:
        return self.args.get_path_to_root()


    # --------------------------------------------------------------------------
    def get_arg_keys(self) -> list[str]:
        return self.args.arg_keys()


    # --------------------------------------------------------------------------
    def help_and_exit(self, exit_code: int, *err_messages: str):
        self.args.help_and_exit(exit_code, *err_messages)


    # --------------------------------------------------------------------------
    def arg_toggle(self, key: str) -> bool:
        """
        When an optional flag value is absent, this will return `True`
        (since the flag was used, but no value was attached).
        """
        return self.args.get_user_values(key).get_bool()


    # --------------------------------------------------------------------------
    def arg_str(self, key: str, default: str = None) -> str | None:
        """
        Returns `default` when an optional positional value is absent
        (and no other default value is specified in the FYR file).
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_strs()[0]


    # --------------------------------------------------------------------------
    def arg_str_list(self, key: str) -> list[str]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_strs()


    # --------------------------------------------------------------------------
    def arg_path(self,
        key: str, default: Path = None,
        assertion: fy.PathAssertion = fy.PathAssertion.NO_ASSERTION,
    ) -> Path | None:
        """
        Returns `default` when an optional positional value is absent
        (and no other default value is specified in the FYR file).
        Otherwise, asserts the validity of the paths using `assertion`.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default

        errs = assertion(uvs)
        if errs: self.help_and_exit(1, *(err.get_error() for err in errs))

        return uvs.get_paths()[0]


    # --------------------------------------------------------------------------
    def arg_path_list(self,
        key: str,
        assertion: fy.PathAssertion = fy.PathAssertion.NO_ASSERTION,
    ) -> Path | None:
        """
        Returns an empty list when optional positional values are absent.
        Asserts the validity of the paths using `assertion`.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return []

        errs = assertion(uvs)
        if errs: self.help_and_exit(1, *(err.get_error() for err in errs))

        return uvs.get_paths()


    # --------------------------------------------------------------------------
    def arg_int(self, key: int, default: int = None) -> int | None:
        """
        Returns `default` when an optional positional value is absent
        (and no other default value is specified in the FYR file).
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_ints()[0]


    # --------------------------------------------------------------------------
    def arg_int_list(self, key: int) -> list[int]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_ints()


    # --------------------------------------------------------------------------
    def arg_float(self, key: float, default: float = None) -> float | None:
        """
        Returns `default` when an optional positional value is absent
        (and no other default value is specified in the FYR file).
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_floats()[0]


    # --------------------------------------------------------------------------
    def arg_float_list(self, key: float) -> list[float]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_floats()


# //////////////////////////////////////////////////////////////////////////////
