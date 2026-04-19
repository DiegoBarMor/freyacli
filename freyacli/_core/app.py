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
        You can use the methods `get_path_to_root`, `get_arg_keys` and `get_arg_value` to access the parsed arguments.
        """
        pass


    # --------------------------------------------------------------------------
    def get_path_to_root(self) -> list[str]:
        return self.args.get_path_to_root()


    # --------------------------------------------------------------------------
    def get_arg_keys(self) -> list[str]:
        return self.args.get_arg_keys()


    # --------------------------------------------------------------------------
    def get_arg_value(self, key: str):
        return self.args.get_arg_value(key)



# //////////////////////////////////////////////////////////////////////////////
