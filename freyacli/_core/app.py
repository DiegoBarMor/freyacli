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
    def arg_keys(self) -> list[str]:
        return self.args.arg_keys()


    # --------------------------------------------------------------------------
    def help_and_exit(self, exit_code: int, *err_messages: str):
        self.args.help_and_exit(exit_code, *err_messages)


    # --------------------------------------------------------------------------
    def get_arg_toggle(self, key: str) -> bool:
        """
        When an optional flag value is absent, this will return `True`
        (since the flag was used, but no value was attached).
        """
        return self.args.get_user_values(key).get_bool()


    # --------------------------------------------------------------------------
    def get_arg_bool(self, key: str, default = None) -> bool:
        """
        Note: Flags with no value attached always store a boolean value.
        (refer to `App.get_arg_toggle()`)
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_bool()


    # --------------------------------------------------------------------------
    def get_arg_str(self, key: str, default = None) -> str | None:
        """
        Returns `default` when an optional positional value is absent.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_strs()[0]


    # --------------------------------------------------------------------------
    def get_arg_str_list(self, key: str) -> list[str]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_strs()


    # --------------------------------------------------------------------------
    def get_arg_path(self,
        key: str, default = None,
        assertion: fy.PathAssertion = fy.PathAssertion.NO_ASSERTION,
        allow_none: bool = False
    ) -> Path | None:
        """
        Returns `default` when an optional positional value is absent (when `allow_none` is True).
        Asserts the validity of the paths using `assertion`.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty() and allow_none: return default

        errs = assertion(uvs, allow_none)
        if errs: self.help_and_exit(1, *(err.get_error() for err in errs))

        return uvs.get_paths()[0]


    # --------------------------------------------------------------------------
    def get_arg_path_list(self,
        key: str,
        assertion: fy.PathAssertion = fy.PathAssertion.NO_ASSERTION,
        allow_none: bool = False
    ) -> Path | None:
        """
        Returns `default` when an optional positional value is absent (when `allow_none` is True).
        Asserts the validity of the paths using `assertion`.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty() and allow_none: return []

        errs = assertion(uvs, allow_none)
        if errs: self.help_and_exit(1, *(err.get_error() for err in errs))

        return uvs.get_paths()


    # --------------------------------------------------------------------------
    def get_arg_int(self, key: int, default = None) -> int | None:
        """
        Returns `default` when an optional positional value is absent.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_ints()[0]


    # --------------------------------------------------------------------------
    def get_arg_int_list(self, key: int) -> list[int]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_ints()


    # --------------------------------------------------------------------------
    def get_arg_float(self, key: float, default = None) -> float | None:
        """
        Returns `default` when an optional positional value is absent.
        """
        uvs = self.args.get_user_values(key)
        if uvs.is_empty(): return default
        return uvs.get_floats()[0]


    # --------------------------------------------------------------------------
    def get_arg_float_list(self, key: float) -> list[float]:
        """
        Returns an empty list when optional positional values are absent.
        """
        return self.args.get_user_values(key).get_floats()


    # --------------------------------------------------------------------------
    def _assert_uvs_paths(self,
        uvs: fy.UserValue, assertion: fy.PathAssertion, allow_none: bool
    ) -> None:
        errors = assertion(uvs, allow_none)
        if any(errors): self.help_and_exit(1, *(err.err_message for err in errors))


# //////////////////////////////////////////////////////////////////////////////
