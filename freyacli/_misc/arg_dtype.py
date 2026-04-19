from enum import Enum, auto

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ArgDType(Enum):
    NONE   = auto()
    TOGGLE = auto()
    STR    = auto()
    PATH   = auto()
    FLOAT  = auto()
    INT    = auto()

    # --------------------------------------------------------------------------
    @classmethod
    def from_str(cls, s: str | None) -> "ArgDType":
        if s is None: return cls.NONE
        s = s.lower()
        if not s:        return cls.TOGGLE
        if s == "str":   return cls.STR
        if s == "path":  return cls.PATH
        if s == "float": return cls.FLOAT
        if s == "int":   return cls.INT
        raise fy.FreyaSyntaxError(f"Invalid flag type specified: '{s}'")


    # --------------------------------------------------------------------------
    def stores_data(self) -> bool:
        return self != ArgDType.TOGGLE


# //////////////////////////////////////////////////////////////////////////////
