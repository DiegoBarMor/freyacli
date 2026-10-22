from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class UserValues:
    def __init__(self):
        self.dtype: fy.ArgDType = fy.ArgDType.NONE

        self._data_toggle: bool = False # a flag is either provided or not; there's no "list of values" here
        self._data_str:   list[str  ] = []
        self._data_path:  list[Path ] = []
        self._data_int:   list[int  ] = []
        self._data_float: list[float] = []

        self._is_wrong: bool = False
        self._err_msg: str = "" # stores information about an error when parsing user-provided argument values.

    # --------------------------------------------------------------------------
    @classmethod
    def init_parse(cls, dtype: fy.ArgDType, raw_values: list[str], arg_name: str) -> "UserValues":
        obj = cls()
        obj.dtype = dtype

        if dtype == fy.ArgDType.STR:
            obj._data_str = [v.strip('"').strip("'") for v in raw_values]
            return obj

        if dtype == fy.ArgDType.PATH:
            try: obj._data_path = [Path(v) for v in raw_values]
            except TypeError as e:
                idx = str(e).find("not")
                return fy.UserValues.init_wrong(
                    f"The specified path with type '{str(e)[idx:]}' is not a valid path."
                )
            return obj

        if dtype == fy.ArgDType.INT:
            try: obj._data_int = [int(v) for v in raw_values]
            except ValueError as e:
                idx = str(e).find(':')
                return fy.UserValues.init_wrong(
                    f"Argument '{arg_name}' expected an integer value, but got{str(e)[idx:]}"
                )
            return obj

        if dtype == fy.ArgDType.FLOAT:
            try: obj._data_float = [float(v) for v in raw_values]
            except ValueError:
                idx = str(e).find(':')
                return fy.UserValues.init_wrong(
                f"Argument '{arg_name}' expected a float value, but got{str(e)[idx:]}"
            )
            return obj

        if dtype == fy.ArgDType.NONE:
            raise fy.FreyaSyntaxError(f"Argument '{arg_name}' doesn't accept any values, but somehow got {raw_values}.")

        if dtype == fy.ArgDType.TOGGLE:
            if not raw_values: return obj
            raise fy.FreyaSyntaxError(
                "`UserValues.init_parse` method shouldn't handle flags of type TOGGLE. " +\
                f"It somehow got argument '{arg_name}' of type TOGGLE with raw_values={raw_values}."
            )

        raise fy.FreyaSyntaxError(f"Unkown dtype '{dtype}' for argument '{arg_name}'.")

    # --------------------------------------------------------------------------
    @classmethod
    def init_empty(cls) -> "UserValues":
        """Same as simply instantiating via `UserValues()`. Added for consistency with other constructors."""
        return cls()

    # --------------------------------------------------------------------------
    @classmethod
    def init_toggle(cls, value: bool) -> "UserValues":
        obj = cls()
        obj.dtype = fy.ArgDType.TOGGLE
        obj._data_toggle = value
        return obj

    # --------------------------------------------------------------------------
    @classmethod
    def init_wrong(cls, err_msg: str = "") -> "UserValues":
        obj = cls()
        obj._is_wrong = True
        obj._err_msg = err_msg
        return obj

    # --------------------------------------------------------------------------
    def assert_dtype(self, dtype: fy.ArgDType, arg_name: str = "") -> None:
        """
        Useful to prevent developers from using the wrong getter for the user value data.
        """
        if self.dtype != dtype: raise fy.FreyaSyntaxError(
            f"Attempted to retrieve {dtype.name} data from '{arg_name}' user value with dtype={self.dtype}"
        )

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

    # --------------------------------------------------------------------------
    def set_bool(self, val: bool) -> None:
        self._data_toggle = val


# //////////////////////////////////////////////////////////////////////////////
