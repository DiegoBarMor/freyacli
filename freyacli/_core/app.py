import os
from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class App:
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
    def run(self):
        print("Do something...")
        print(self.args.args)


# //////////////////////////////////////////////////////////////////////////////
