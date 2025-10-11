import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ParserHelp:
    def __init__(self, str_help: str):
        self.__str_help = str_help

    # --------------------------------------------------------------------------
    def parse(self):
        for line in self.__str_help.splitlines():
            print(f"HELP: {line}")  # [WIP]


# //////////////////////////////////////////////////////////////////////////////
