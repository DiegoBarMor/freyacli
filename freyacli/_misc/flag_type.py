from enum import Enum, auto

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class FlagType(Enum):
    TOGGLE = auto()
    STR    = auto()
    PATH   = auto()
    FLOAT  = auto()
    INT    = auto()

    # --------------------------------------------------------------------------
    @classmethod
    def from_str(cls, s: str) -> "FlagType":
        s = s.lower()
        if not s:        return cls.TOGGLE
        if s == "str":   return cls.STR
        if s == "path":  return cls.PATH
        if s == "float": return cls.FLOAT
        if s == "int":   return cls.INT
        raise fy.FreyaSyntaxError(f"Invalid flag type specified: '{s}'")


    # --------------------------------------------------------------------------
    def stores_data(self) -> bool:
        return self != FlagType.TOGGLE


# //////////////////////////////////////////////////////////////////////////////
