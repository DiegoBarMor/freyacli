import os
import sys
from pathlib import Path

import os, sys; sys.path.insert(0, os.getcwd()) # allow imports from root folder
import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class App(fy.App):
    _APP_NAME = "volgrids"
    _VERSION = "1.2.3"

    # --------------------------------------------------------------------------
    def run(self):
        self.assert_paths(
            keys_file_in = ["path_in", "paths_in"]
        )

        print("A: Do something with the path of subcommands:")
        print(f"\t{self.get_path_to_root()}")

        print()
        print("B: Do something with the keys of the stored values:")
        keys = self.arg_keys()
        print(f"\t{keys}")

        print()
        print("C: Use the keys to do something with the stored values:")
        for key in keys:
            value = self.get_arg_value(key)
            print(f"\t{key} = {value} ({type(value)})")

        print()
        print("D: Override the user stored values:")
        if "path_chem" in keys and self.get_arg_value("path_chem") is None:
            self.set_arg_value("path_chem", Path(__file__).parent)
            print("Overriden 'path_chem':", self.get_arg_value("path_chem"))


################################################################################
if __name__ == "__main__":
    dir_example = Path(__file__).parent
    App(sys.argv,
        path_fyr = dir_example / "fy_rules.fyr",
        path_fyh = dir_example / "fy_help.fyh",
    ).run()


################################################################################
