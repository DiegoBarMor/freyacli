import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class Flag(fy.Arg):
    def __init__(self, name_long: str, name_short: str, help_str: str = ""):
        super().__init__(name_long, help_str, optional = True)
        self._name_long = name_long
        self._name_short = name_short
        assert len(name_short) == 1, "Flag short name must be a single character"

    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Flag(name_long={self._name_long}, name_short={self._name_short})"

# //////////////////////////////////////////////////////////////////////////////
