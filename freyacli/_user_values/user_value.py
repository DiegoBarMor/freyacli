from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class UserValue:
    def __init__(self):
        self._data_any: str = None # even if it's referred as "Any", generic data obtained from the CLI are strings
        self._data_toggle: bool = None
        self._data_str: str = None
        self._data_path: Path = None
        self._data_int: int = None
        self._data_float: float = None

        self._is_wrong: bool = False
        self._err_msg: str = "" # stores information about an error when parsing user-provided argument values.

    # --------------------------------------------------------------------------
    @classmethod
    def parse_value(cls) -> "UserValue":
        obj = cls()
        ...
        return obj

    # --------------------------------------------------------------------------
    @classmethod
    def init_wrong(cls, err_msg: str = "") -> "UserValue":
        obj = cls()
        obj._is_wrong = True
        obj._err_msg = err_msg
        return obj

    # --------------------------------------------------------------------------
    def is_wrong(self) -> bool:
        return self._is_wrong

    # --------------------------------------------------------------------------
    def get_error(self) -> str:
        return self._err_msg


# //////////////////////////////////////////////////////////////////////////////
