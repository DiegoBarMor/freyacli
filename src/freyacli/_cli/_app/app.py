from pathlib import Path

from .._utils.safe_io import safe_read_file
import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class App:
    def __init__(self, path_cli: Path, path_help: Path = None):
        str_cli = safe_read_file(path_cli)
        str_help = '' if path_help is None else \
            safe_read_file(path_help)

        self._parser_cli = fy.ParserCli(str_cli)
        self._parser_help = fy.ParserHelp(str_help)

        self._parser_cli.parse()
        self._parser_help.parse()

    # --------------------------------------------------------------------------


# //////////////////////////////////////////////////////////////////////////////
