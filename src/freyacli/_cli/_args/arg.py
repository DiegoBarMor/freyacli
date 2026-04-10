from abc import ABC

# //////////////////////////////////////////////////////////////////////////////
class Arg(ABC):
    def __init__(self, name: str, help_str: str = "", optional: bool = False):
        self._name = name
        self._help_str = help_str
        self._optional = optional

    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Arg(name={self._name}, optional={self._optional})"


# //////////////////////////////////////////////////////////////////////////////
