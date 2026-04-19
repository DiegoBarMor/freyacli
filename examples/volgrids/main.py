import os
import sys
from pathlib import Path

import os, sys; sys.path.insert(0, os.getcwd()) # allow imports from root folder
import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class App(fy.App):
    _APP_NAME = "volgrids"
    _VERSION = "1.2.3"

    def run(self):
        values = self.args._user_values
        print(*values.items(), sep="\n")
        # self.args.help_and_exit(1) # [WIP]


################################################################################
if __name__ == "__main__":
    dir_example = Path(__file__).parent
    App(sys.argv,
        path_fyr = dir_example / "fy_rules.fyr",
        path_fyh = dir_example / "fy_help.fyh",
    ).run()


################################################################################
