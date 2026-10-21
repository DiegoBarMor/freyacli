from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class UserValue:
    def __init__(self):
        self._has_data: bool = False

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
    def init_parse(cls, dtype: fy.ArgDType, raw_value: str, arg_name: str) -> "UserValue":
        obj = cls()
        obj._has_data = True

        if dtype == fy.ArgDType.ANY or dtype == fy.ArgDType.STR:
            obj._data_str = raw_value.strip('"').strip("'")
            return obj

        if dtype == fy.ArgDType.PATH:
            try: obj._data_path = Path(raw_value)
            except ValueError: return fy.UserValue.init_wrong(
                f"Argument '{arg_name}' couldn't be parsed into a Python Path object.."
            )
            return obj

        if dtype == fy.ArgDType.INT:
            try: obj._data_int = int(raw_value)
            except ValueError: return fy.UserValue.init_wrong(
                f"Argument '{arg_name}' expected an integer value, but got '{raw_value}'."
            )
            return obj

        if dtype == fy.ArgDType.FLOAT:
            try: obj._data_float = float(raw_value)
            except ValueError: return fy.UserValue.init_wrong(
                f"Argument '{arg_name}' expected a float value, but got '{raw_value}'."
            )
            return obj

        if dtype == fy.ArgDType.NONE:
            raise fy.FreyaSyntaxError(f"Argument doesn't accept any values, but somehow got '{raw_value}'.")

        if dtype == fy.ArgDType.TOGGLE:
            raise fy.FreyaSyntaxError(f"Argument is a flag of type TOGGLE and doesn't accept any values, but somehow got '{raw_value}'.")

        raise fy.FreyaSyntaxError(f"Unkown dtype '{dtype}'.")

    # --------------------------------------------------------------------------
    @classmethod
    def init_empty(cls) -> "UserValue":
        """Same as simply instantiating via `UserValue()`. Added for consistency with other constructors."""
        obj = cls()
        return obj

    # --------------------------------------------------------------------------
    @classmethod
    def init_toggle(cls, value: bool) -> "UserValue":
        obj = cls()
        obj._has_data = True
        obj._data_toggle = value
        return obj

    # --------------------------------------------------------------------------
    @classmethod
    def init_wrong(cls, err_msg: str = "") -> "UserValue":
        obj = cls()
        obj._is_wrong = True
        obj._err_msg = err_msg
        return obj

    # --------------------------------------------------------------------------
    def is_empty(self) -> bool:
        return not self._has_data

    # --------------------------------------------------------------------------
    def is_wrong(self) -> bool:
        return self._is_wrong

    # --------------------------------------------------------------------------
    def get_error(self) -> str:
        return self._err_msg


# //////////////////////////////////////////////////////////////////////////////
