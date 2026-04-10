import re
import freyacli as fy

from enum import Enum, auto

# //////////////////////////////////////////////////////////////////////////////
class State(Enum):
    FIRST_CHAR = auto()
    ARG_OPT_ENDED = auto()
    ID_STARTED = auto()
    ID_ENDED = auto()
    ALIASES_STARTED = auto()
    ALIAS_SHORT = auto()
    ALIAS_LONG = auto()
    ALIASES_ENDED = auto()
    TYPES = auto()

# //////////////////////////////////////////////////////////////////////////////
class StrDelim(Enum):
    NONE = auto()
    SINGLE = auto()
    DOUBLE = auto()

    @classmethod
    def match_char(cls, char):
        match char:
            case "'": return cls.SINGLE
            case '"': return cls.DOUBLE
            case _:   return cls.NONE

# //////////////////////////////////////////////////////////////////////////////
class Argument:
    def __init__(self):
        pass


# //////////////////////////////////////////////////////////////////////////////
class CharCli:
    ARG_OPTIONAL = '~'
    ALIASES_START = '['
    ALIAS_SHORT_DELIM = '\''
    ALIAS_LONG_DELIM = '"'
    ALIASES_END = ']'

    @classmethod
    def is_arg_optional(cls, char):
        return char == cls.ARG_OPTIONAL

    @staticmethod
    def is_valid_id(char):
        return char.isalnum() or char == '_'

    @classmethod
    def is_aliases_start(cls, char):
        return char == cls.ALIASES_START

    @classmethod
    def is_alias_short(cls, char):
        return char == cls.ALIAS_SHORT_DELIM

    @classmethod
    def is_alias_long(cls, char):
        return char == cls.ALIAS_LONG_DELIM
        
    @classmethod
    def is_aliases_end(cls, char):
        return char == cls.ALIASES_END

    
    
# //////////////////////////////////////////////////////////////////////////////
class ParserCli:

    def __init__(self, str_cli: str):
        self._str_cli = str_cli

        self._line = ""        
        self._state = State.FIRST_CHAR

        self._str_delim = StrDelim.NONE
        
        self._current_argument = None
        self._buffer_arg_opt: bool = False
        self._buffer_id: str = ""
        self._buffer_aliases: list[str,...] = []

    
    # --------------------------------------------------------------------------
    def parse(self):
        """
        arg_id["flag", "aliases"].TYPE 
        arg_id["flag", "aliases"].(T0|T1|T2)
        """

        
        for line in self._str_cli.splitlines():
            print(f"CLI: {line}") # [WIP]

            if line.startswith('@'): continue # [WIP]

            self._state = State.FIRST_CHAR
            self._line = line.strip()
            self._reset_buffers()
            self._parse_line()
            
            
            if line.startswith('}'): continue





    
    # --------------------------------------------------------------------------
    def _parse_line(self):
        for i,char in enumerate(self._line):
            match self._state:
                case State.FIRST_CHAR: self._parse_first_char(char)
                case State.ARG_OPT_ENDED: self._parse_arg_opt_ended(char)
                case State.ID_STARTED: self._parse_id_started(char)
                case State.ID_ENDED: self._parse_id_ended(char)
                case State.ALIASES_STARTED: self._parse_aliases_started(char)
                case State.ALIAS_SHORT: self._parse_alias_short(char)
                case State.ALIAS_LONG: self._parse_alias_long(char)
                case State.ALIASES_ENDED: self._parse_aliases_ended(char)
                case State.TYPES: self._parse_types(char)


    # --------------------------------------------------------------------------
    def _parse_first_char(self, char):
        if char == '@': # WIP
            if self._current_argument is None:
                self._raise_error("Can't branch with '@' without specifying an argument to branch.")
        if char == '}': pass # WIP
        
        self._buffer_arg_opt = CharCli.is_arg_optional(char)
        self._state = State.ARG_OPT_ENDED


    # --------------------------------------------------------------------------
    def _parse_arg_opt_ended(self, char):
        if char.isspace():
            return

        if CharCli.is_valid_id(char):
            self._buffer_id += char
            self._state = State.ID_STARTED
            return
    
        self._raise_error(f"Invalid character in argument ID: '{char}'")
        
            
    # --------------------------------------------------------------------------
    def _parse_id_started(self, char):
        if char.isspace():
            self._state = State.ID_ENDED
            return
    
        if CharCli.is_aliases_start(char):
            self._state = State.ALIASES_STARTED
            return

        if CharCli.is_valid_id(char):
            self._buffer_id += char
            return

        self._raise_error(f"Invalid character in argument ID: '{char}'")

    
            
    # --------------------------------------------------------------------------
    def _parse_id_ended(self, char): 
        if char.isspace():
            return

        if CharCli.is_aliases_start(char):
            self._state = State.ALIASES_STARTED
            return

        self._raise_error("Can't have spaces in argument ID")
        
        
    # --------------------------------------------------------------------------
    def _parse_aliases_started(self, char):
        if char.isspace():
            return
    
        if CharCli.is_alias_short(char):
            self._state = State.ALIAS_SHORT

        if CharCli.is_alias_long(char):
            self._state = State.ALIAS_LONG
    
        if CharCli.is_aliases_end(char):
            self._state = State.ALIASES_ENDED


    # --------------------------------------------------------------------------
    def _parse_alias_short(self, char): 
        pass
        
    # --------------------------------------------------------------------------
    def _parse_alias_long(self, char): 
        pass
        
    # --------------------------------------------------------------------------
    def _parse_aliases_ended(self, char): 
        pass
    
        
    # --------------------------------------------------------------------------
    def _parse_types(self, char): 
        pass

    # --------------------------------------------------------------------------
    def _reset_buffers(self):
        self._buffer_arg_opt = False
        self._buffer_id  = ""
        self._buffer_aliases.clear()
        

    # --------------------------------------------------------------------------
    def _raise_error(self, message):
        raise SyntaxError(f"\n\nError while parsing the CLI line:\n  {self._line}\n\nReason: {message}")
    

# //////////////////////////////////////////////////////////////////////////////
