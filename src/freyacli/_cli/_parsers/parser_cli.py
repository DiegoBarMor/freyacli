import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ParserCli:
    def __init__(self, str_cli: str):
        self._str_cli = str_cli

    # --------------------------------------------------------------------------
    def parse(self):
        for line in self._str_cli.splitlines():
            print(f"CLI: {line}") # [WIP]


# //////////////////////////////////////////////////////////////////////////////
