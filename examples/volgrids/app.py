from pathlib import Path

from enum import Enum, auto

# //////////////////////////////////////////////////////////////////////////////
class FlagType(Enum):
    BOOL  = auto()
    STR   = auto()
    PATH  = auto()
    FLOAT = auto()
    INT   = auto()

    # --------------------------------------------------------------------------
    @classmethod
    def from_str(cls, s: str) -> "FlagType":
        s = s.lower()
        if not s:        return cls.BOOL
        if s == "str":   return cls.STR
        if s == "path":  return cls.PATH
        if s == "float": return cls.FLOAT
        if s == "int":   return cls.INT
        CLIFileError.parsing_err(f"Invalid flag type specified: '{s}'")


# //////////////////////////////////////////////////////////////////////////////
class CLIFileError(SyntaxError):
    # --------------------------------------------------------------------------
    @classmethod
    def parsing_err(cls, msg: str):
        raise cls(f"Error parsing CLI file string: {msg}")

    # --------------------------------------------------------------------------
    @classmethod
    def assert_split(cls, s: str, char_split: str, expected_len: int):
        splitted = s.split(char_split)
        if len(splitted) == expected_len: return splitted
        cls.parsing_err(f"Invalid substring found inside argument rule: '{s}'")


# //////////////////////////////////////////////////////////////////////////////
class ArgumentRule:
    def __init__(self, raw_rule: str):
        self._raw_rule = raw_rule
        self.is_optional: bool
        self.name: str
        self.is_positional: bool
        self.flag_short: str
        self.flag_long: str
        self.kw_is_optional: bool
        self.kw_default_val: str
        self.flag_type: FlagType
        self.n_args: int

        self.is_optional = raw_rule.startswith('~')
        self._parse_flag_type(self._parse_n_args(
            self._parse_flags(self._parse_name(
                self._parse_default_value(raw_rule)
            ))
        ))


    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Arg(opt={self.is_optional} posit={self.is_positional} fs={self.flag_short} fl={self.flag_long} "+\
            f"opt_kw={self.kw_is_optional} default={self.kw_default_val} ftype={self.flag_type} nargs={self.n_args})"


    # --------------------------------------------------------------------------
    def _parse_default_value(self, buffer: str) -> str:
        idx = buffer.find('=')
        if idx == -1:
            self.kw_default_val = ""
            return buffer
        self.kw_default_val = buffer[idx+1:]
        return buffer[:idx]


    # --------------------------------------------------------------------------
    def _parse_name(self, buffer: str) -> str:
        name, buffer = CLIFileError.assert_split(buffer, '[', 2)
        self.name = name[int(self.is_optional):]
        return buffer


    # --------------------------------------------------------------------------
    def _parse_flags(self, buffer: str) -> str:
        flags, buffer = CLIFileError.assert_split(buffer, ']', 2)
        self.is_positional = not flags

        if self.is_positional:
            self.flag_short = ""
            self.flag_long = ""
            return buffer

        self.flag_short, self.flag_long = CLIFileError.assert_split(flags, ',', 2)
        if len(self.flag_short) > 1:
            CLIFileError.parsing_err(f"Short flags should be 1 character long, but got '{self.flag_short}'.")

        return buffer


    # --------------------------------------------------------------------------
    def _parse_n_args(self, buffer: str) -> str:
        if not buffer:
            if self.kw_default_val:
                CLIFileError.parsing_err(f"Flags with no arguments can't have a default value ('{self._raw_rule}')")
            if self.is_positional:
                CLIFileError.parsing_err(f"Positional arguments must specify type and number of arguments ('{self._raw_rule}')")

            self.kw_is_optional = False
            self.n_args = 0
            return ""

        n_args, buffer = CLIFileError.assert_split(buffer, '.', 2)
        self.kw_is_optional = n_args.startswith('~')

        if self.kw_is_optional: n_args = n_args[1:]

        if n_args == '*':
            self.n_args = -1
            return buffer

        try:
            self.n_args = int(n_args)
        except ValueError:
            CLIFileError.parsing_err(f"Invalid number of arguments specified: '{n_args}'")

        return buffer


    # --------------------------------------------------------------------------
    def _parse_flag_type(self, buffer: str) -> None:
        self.flag_type = FlagType.from_str(buffer)



# //////////////////////////////////////////////////////////////////////////////
class Node:
    def __init__(self, name: str, parent: "Node|None"):
        self.name = name
        self.parent: "Node|None" = parent
        self.children: dict[str, "Node"] = {}
        self.depth = 0 if parent is None else parent.depth + 1
        self.rules: dict[str, ArgumentRule] = {}

    # --------------------------------------------------------------------------
    def __repr__(self):
        values = ','.join('' if v is None else str(v) for v in self.children.values())
        return f"Node({self.depth}:{self.name}){{{values if values else ''}}}"

    # --------------------------------------------------------------------------
    def __getitem__(self, name: str) -> "Node":
        if name not in self.children:
            CLIFileError.parsing_err(f"Branch '{name}' is not defined in the CLI rules.")
        return self.children[name]

    # --------------------------------------------------------------------------
    def add_child(self, name: str) -> "Node":
        self._assert_unique_child(name)
        child = Node(name, self)
        self.children[name] = child
        return child

    # --------------------------------------------------------------------------
    def is_leaf(self) -> bool:
        return not self.children


    # --------------------------------------------------------------------------
    def _assert_unique_child(self, name: str):
        if name in self.children:
            CLIFileError.parsing_err(f"Duplicate child branch '{name}' specified inside the same branch.")


# //////////////////////////////////////////////////////////////////////////////
class FYRParser:
    def __init__(self, raw_rules: str):
        rules = self._preprocess_cli_rules(raw_rules)
        self.tree = Node('', None)
        self.node = self.tree
        self.build_rules_tree(rules)


    # --------------------------------------------------------------------------
    @classmethod
    def read_cli(cls, path_cli: str|Path):
        return cls(Path(path_cli).read_text())


    # --------------------------------------------------------------------------
    def build_rules_tree(self, rules: str):
        node: Node = self.tree
        for token in rules.split():
            if token.startswith('@'):
                name = token[1:]
                node = node.add_child(name)
                continue

            if token == "!@":
                if node.depth == 0: CLIFileError.parsing_err("Unexpected '!@' token found outside of any branch.")
                node = node.parent
                continue

            arg = ArgumentRule(token)
            if arg.name in node.rules:
                CLIFileError.parsing_err(f"Duplicate definition of '{arg}' argument rule")

            node.rules[arg.name] = arg

        if node != self.tree:
            CLIFileError.parsing_err(f"Unterminated branch (missing !@ keyword {node.depth} times)")



    # --------------------------------------------------------------------------
    @classmethod
    def _preprocess_cli_rules(cls, rules: str):
        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def get_next_macro_idxs(s: str) -> tuple[int, int]|None:
            i0 = s.find("!def")
            if i0 == -1: return

            i1 = s.find("!fed")
            if i1 == -1: CLIFileError.parsing_err("!def macro is missing the '!fed' closure.")

            return i0,i1

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def get_text_around_macro(s: str, idxs: tuple[int, int]) -> str:
            return s[:idxs[0]] + s[idxs[1]+4:]

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def get_text_inside_macro(s: str, idxs: tuple[int, int]) -> str:
            return s[idxs[0]+4:idxs[1]]

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def get_macros(s: str) -> dict[str, str]:
            macros = {}
            s_lower = s.lower()
            while s_lower:
                idxs = get_next_macro_idxs(s_lower)
                if idxs is None: break
                macro_split = get_text_inside_macro(s, idxs).split()
                s = get_text_around_macro(s, idxs)
                s_lower = get_text_around_macro(s_lower, idxs)

                if not macro_split:
                    CLIFileError.parsing_err("A !def macro is missing its name.")

                macro_key = macro_split[0]
                macro_val = "" if len(macro_split) == 1 \
                    else '\n'.join(macro_split[1:])

                if "!def" in macro_val:
                    CLIFileError.parsing_err("Nested !def macros are not allowed")

                if macro_key in macros:
                    CLIFileError.parsing_err(f"Duplicate definition of '{macro_key}' macro")

                macros[macro_key] = macro_val
            return macros

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def apply_macros(s: str):
            macros = get_macros(s)
            for macro_key, macro_val in macros.items():
                s = s.replace(f"!use:{macro_key}", macro_val)

            while s:
                idxs = get_next_macro_idxs(s)
                if idxs is None: break
                s = get_text_around_macro(s, idxs)

            return s

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        without_comments = (
            row.split('#')[0].strip() for row in rules.split('\n')
        )
        return apply_macros(
            '\n'.join(filter(None, without_comments))
        )


################################################################################
if __name__ == "__main__":
    dir_example = Path(__file__).parent
    parser = FYRParser.read_cli(dir_example / "fy_rules.fyr")
    print(*parser.tree["smiffer"]["rna"].rules.items(), sep = '\n')
    print()
    print(*parser.tree["vgtools"]["convert"].rules.items(), sep = '\n')
    print()
    print(*parser.tree["vgtools"]["compare"].rules.items(), sep = '\n')


################################################################################
