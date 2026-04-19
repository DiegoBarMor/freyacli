import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ArgsParser:
    def __init__(self, fy_parser: fy.FreyaParser, app_name: str, version: str):
        self.args = {}
        self._app_name = app_name
        self._version = version

        self._fy_parser = fy_parser
        self._current_node = fy_parser.tree

    # --------------------------------------------------------------------------
    def parse_args(self, args: list[str]):
        if not args: raise fy.FreyaSyntaxError(
            "Argument list shouldn't be empty. At least the application name should be specified (e.g. sys.argv[0])."
        )
        self.py_name = args[0]
        self._parse_args(args[1:])


    # --------------------------------------------------------------------------
    def _parse_args(self, args: list[str]) -> None:
        self._current_node = self._fy_parser.tree

        for arg in args:
            if self._current_node.is_leaf():
                self._parse_argument(arg)
                continue

            self._parse_subcommand(arg)

        if not self._current_node.is_leaf(): # [NOTE] execution of the app must currently happen at a leaf node
            self._help_and_exit(1)


    # --------------------------------------------------------------------------
    def _parse_subcommand(self, next_subcommand: str):
        if next_subcommand not in self._current_node.children:
            self._help_and_exit(1, f"Unrecognized command: '{next_subcommand}'.")

        self._current_node = self._current_node.get_child(next_subcommand)


    # --------------------------------------------------------------------------
    def _parse_argument(self, arg: str):
        # [TODO]
        print("LEAF", arg)
        self._help_and_exit(1)


    # --------------------------------------------------------------------------
    def _help_and_exit(self, exit_code: int, err_message: str = ""):
        if err_message: err_message = fy.Color.red(
            fy.HelpStr(err_message).nl_surround(), bright = False
        )
        print('\n'.join((
            f"{self._app_name} ({fy.Color.red('v'+self._version)}). Usage:",
            self._current_node.str_help_long(self.py_name),
            err_message,
        )))
        exit(exit_code)


# //////////////////////////////////////////////////////////////////////////////
