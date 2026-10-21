from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class UserValue:
    def __init__(self):
        self._has_data: bool = False

        self._data_toggle: bool = False # a flag is either provided or not; there's no "list of values" here
        self._data_str:   list[str  ] = []
        self._data_path:  list[Path ] = []
        self._data_int:   list[int  ] = []
        self._data_float: list[float] = []

        self._is_wrong: bool = False
        self._err_msg: str = "" # stores information about an error when parsing user-provided argument values.

    # --------------------------------------------------------------------------
    @classmethod
    def init_parse(cls, dtype: fy.ArgDType, raw_values: list[str], arg_name: str) -> "UserValue":
        obj = cls()
        obj._has_data = True

        if dtype == fy.ArgDType.ANY or dtype == fy.ArgDType.STR:
            obj._data_str = [v.strip('"').strip("'") for v in raw_values]
            return obj

        if dtype == fy.ArgDType.PATH:
            try: obj._data_path = [Path(v) for v in raw_values]
            except TypeError as e:
                idx = str(e).find("not")
                return fy.UserValue.init_wrong(
                    f"The specified path with type '{str(e)[idx:]}' is not a valid path."
                )
            return obj

        if dtype == fy.ArgDType.INT:
            try: obj._data_int = [int(v) for v in raw_values]
            except ValueError as e:
                idx = str(e).find(':')
                return fy.UserValue.init_wrong(
                    f"Argument '{arg_name}' expected an integer value, but got{str(e)[idx:]}"
                )
            return obj

        if dtype == fy.ArgDType.FLOAT:
            try: obj._data_float = [float(v) for v in raw_values]
            except ValueError:
                idx = str(e).find(':')
                return fy.UserValue.init_wrong(
                f"Argument '{arg_name}' expected a float value, but got{str(e)[idx:]}"
            )
            return obj

        if dtype == fy.ArgDType.NONE:
            raise fy.FreyaSyntaxError(f"Argument doesn't accept any values, but somehow got {raw_values}.")

        if dtype == fy.ArgDType.TOGGLE:
            raise fy.FreyaSyntaxError(f"Argument is a flag of type TOGGLE and doesn't accept any values, but somehow got {raw_values}.")

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

    # --------------------------------------------------------------------------
    def get_bool(self) -> bool:
        return self._data_toggle

    # --------------------------------------------------------------------------
    def get_anys(self) -> list[str]:
        return self._data_str

    # --------------------------------------------------------------------------
    def get_strs(self) -> list[str]:
        return self._data_str

    # --------------------------------------------------------------------------
    def get_paths(self) -> list[Path]:
        return self._data_path

    # --------------------------------------------------------------------------
    def get_ints(self) -> list[int]:
        return self._data_int

    # --------------------------------------------------------------------------
    def get_floats(self) -> list[float]:
        return self._data_float


# //////////////////////////////////////////////////////////////////////////////
