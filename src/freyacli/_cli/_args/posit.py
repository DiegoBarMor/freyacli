import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class Posit(fy.Arg):
    def __init__(self, name: str, help_str: str = "", optional: bool = False):
        super().__init__(name, help_str, optional)
        self._branches: dict[str, "fy.Arg"] = {}
        self._branches_help: dict[str, str] = {}

    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Posit(name={self._name}, optional={self._optional})"

    # --------------------------------------------------------------------------
    def branch(self, at_value: str, help_str = "", cli_args: list["fy.Arg"] = ()) -> "Posit":
        assert at_value not in self._branches, f"Value '{at_value}' already has a branch"
        self._branches[at_value] = cli_args
        self._branches_help[at_value] = help_str
        return self

# //////////////////////////////////////////////////////////////////////////////
