import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ArgumentRule:
    def __init__(self, raw_rule: str):
        self._raw_rule = raw_rule
        self._raw_user_value: str = ""
        self.help_str: fy.HelpStr = fy.HelpStr()

        self.name: str
        self.is_positional: bool
        self.is_optional: bool
        self.kw_is_optional: bool
        self.flag_short: str
        self.flag_long: str
        self.default_value: str
        self.flag_type: fy.FlagType
        self.n_args: int

        self.is_optional = raw_rule.startswith('~')

        (buffer,
            self.default_value
        ) = self._parse_default_value(raw_rule)

        (buffer,
            self.name
        ) = self._parse_name(buffer)

        (buffer,
            self.is_positional,
            self.flag_short,
            self.flag_long
        ) = self._parse_flags(buffer)

        (buffer,
            self.kw_is_optional,
            self.n_args
        ) = self._parse_n_args(buffer)

        self.flag_type = fy.FlagType.from_str(buffer)


    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Arg(opt={self.is_optional} posit={self.is_positional} fs={self.flag_short} fl={self.flag_long} "+\
            f"opt_kw={self.kw_is_optional} default={self.default_value} ftype={self.flag_type} nargs={self.n_args} "+\
            f"help='{self.help_str.string[:20]}...')"


    # --------------------------------------------------------------------------
    def _parse_default_value(self, buffer: str) -> tuple[str, str]:
        idx = buffer.find('=')
        if idx == -1: return buffer, ''
        return buffer[:idx], buffer[idx+1:]


    # --------------------------------------------------------------------------
    def _parse_name(self, buffer: str) -> tuple[str, str]:
        name, buffer = self._assert_split_into_2(buffer, '[')
        return buffer, name[int(self.is_optional):]


    # --------------------------------------------------------------------------
    def _parse_flags(self, buffer: str) -> tuple[str, bool, str, str]:
        flags, buffer = self._assert_split_into_2(buffer, ']')
        if not flags: return buffer, True, '', ''

        flag_short, flag_long = self._assert_split_into_2(flags, ',')
        if len(flag_short) > 1:
            raise fy.FreyaSyntaxError(f"Short flags should be 1 character long, but got '{self.flag_short}'.")

        return buffer, False, flag_short, flag_long


    # --------------------------------------------------------------------------
    def _parse_n_args(self, buffer: str) -> tuple[str, bool, int]:
        if not buffer:
            if self.default_value:
                raise fy.FreyaSyntaxError(f"Flags with no arguments can't have a default value ('{self._raw_rule}')")
            if self.is_positional:
                raise fy.FreyaSyntaxError(f"Positional arguments must specify type and number of arguments ('{self._raw_rule}')")

            return "", False, 0

        n_args, buffer = self._assert_split_into_2(buffer, '.')
        kw_is_optional = n_args.startswith('~')

        if kw_is_optional: n_args = n_args[1:]

        if n_args == '*':
            return buffer, kw_is_optional, -1

        if not n_args.isdigit():
            raise fy.FreyaSyntaxError(f"Invalid number of arguments specified: '{n_args}'")

        return buffer, kw_is_optional, int(n_args)


    # --------------------------------------------------------------------------
    def _assert_split_into_2(self, buffer: str, char_split: str) -> tuple[str, str]:
        splitted = buffer.split(char_split)
        if len(splitted) == 2: return splitted
        raise fy.FreyaSyntaxError(f"Invalid substring found inside argument rule: '{self._raw_rule}'")


# //////////////////////////////////////////////////////////////////////////////
