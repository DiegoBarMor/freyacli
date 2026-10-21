from enum import Enum, auto
from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ArgDType(Enum):
    NONE   = auto()
    ANY    = auto()
    TOGGLE = auto()
    STR    = auto()
    PATH   = auto()
    INT    = auto()
    FLOAT  = auto()

    # --------------------------------------------------------------------------
    @classmethod
    def from_str(cls, s: str | None) -> "ArgDType":
        if s is None: return cls.NONE
        s = s.lower()
        if not s:        return cls.TOGGLE
        if s == "any":   return cls.ANY
        if s == "str":   return cls.STR
        if s == "path":  return cls.PATH
        if s == "float": return cls.FLOAT
        if s == "int":   return cls.INT
        raise fy.FreyaSyntaxError(f"Invalid flag type specified: '{s}'")


    # --------------------------------------------------------------------------
    def stores_data(self) -> bool:
        return self != ArgDType.NONE and self != ArgDType.TOGGLE


# //////////////////////////////////////////////////////////////////////////////
