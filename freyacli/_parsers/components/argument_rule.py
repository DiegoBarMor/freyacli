import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ArgumentRule:
    _INDENT_LONG_DESC = 8

    # --------------------------------------------------------------------------
    def __init__(self, raw_rule: str):
        self._raw_rule = raw_rule
        self._raw_user_value: str = ""
        self.help_str: fy.HelpStr = fy.HelpStr()

        self.name: str              # name that will be displayed between <> (e.g. "<value>") in the help string, and used to fetch any given values
        self.is_positional: bool    # True when the argument doesn't need a preceding "flag" (e.g. just "<value>" instead of "--flag <value>")
        self.is_optional: bool      # display with surrounding [] in the help string (e.g. "[<value>]")
        self.kw_is_optional: bool   # these are flags that can optionally have a keyword argument, e.g. "--flag <value>" and "--flag" are both valid. Represented as "--flag [<value>]"
        self.flag_short: str        # must be 1 character long. It's always used with a single preceding dash (e.g. "-f")
        self.flag_long: str         # used with a double preceding dash (e.g. "--flag")
        self.default_value: str     # when a default value is present, it's placed at the beginning of the respective help string, right after the flag type (e.g. "INT (default: 0)").
        self.flag_type: fy.FlagType # placed at the beginning of the help string. TOGGLE type is used for flags with no arguments, and the respective type (e.g. STR, INT) is used for flags with arguments.
        self.n_args: int            # when larger than 1, the help string will display ...; when -1 the argument can be repeated indefinitely; otherwise, the exact number of arguments is displayed after ... (e.g. "--flag <value>...(3)")

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


    # --------------------------------------------------------------------------
    def get_usage_str_positional(self) -> str:
        """Usage string is only relevant for positionals. Flag arguments are summarized as [options...] in the usage string. A more detailed description of them is provided in the longer help string."""

        if not self.is_positional:
            raise fy.FreyaSyntaxError(f"Usage string can only be generated for positional arguments, but got a flag argument ('{self._raw_rule}').")

        buffer = f"<{self.name}{self._get_str_n_args()}>"
        if self.is_optional: buffer = f"[{buffer}]"
        return fy.Color.blue(buffer)

    # --------------------------------------------------------------------------
    def get_help_string_description(self) -> str:
        preffix = ""
        if self.is_optional: preffix += "[optional] "
        if self.flag_type.stores_data():
            preffix += self.flag_type.name
            if self.default_value: preffix += f" (default: {self.default_value})"
            preffix += ". "

        arg_desc = self._get_arg_description()
        long_desc = self.help_str.wrapped_text(
            indent = self._INDENT_LONG_DESC,
            width = fy.WIDTH_TERMINAL - self._INDENT_LONG_DESC,
            preffix = fy.Color.yellow(preffix)
        )
        return f"{arg_desc}\n{self._INDENT_LONG_DESC*' '}{long_desc}"


    # --------------------------------------------------------------------------
    def _get_arg_description(self) -> str:
        buffer = f"<{self.name}{self._get_str_n_args()}>"

        if self.is_positional:
            if self.is_optional: buffer = f"[{buffer}]"
            return fy.Color.blue("    " + buffer)


        if self.kw_is_optional: buffer = f"[{buffer}]"

        if self.is_optional:
            str_flags_0 = "["
            str_flags_1 = "]"
        else:
            str_flags_0 = ""
            str_flags_1 = ""

        flag_short = f"-{self.flag_short}" if self.flag_short else ""
        flag_long  = f"--{self.flag_long}" if self.flag_long  else ""

        str_flags_0 += (
            f"{flag_short}, {flag_long}" if self.flag_long else flag_short
        ) if self.flag_short else flag_long

        buffer = f"    {fy.Color.green(str_flags_0)} {fy.Color.blue(buffer)}"
        if str_flags_1: buffer += fy.Color.green(str_flags_1)
        return buffer


    # --------------------------------------------------------------------------
    def _get_str_n_args(self) -> str:
        if self.n_args == -1: return "..."
        if self.n_args <= 1: return ""
        return f"...({self.n_args})"


# //////////////////////////////////////////////////////////////////////////////
