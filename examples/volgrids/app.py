from pathlib import Path

from enum import Enum, auto

# //////////////////////////////////////////////////////////////////////////////
class FreyaSyntaxError(SyntaxError):
    def __init__(self, msg):
        super().__init__(f"Error parsing FYR string. {msg}")


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
        raise FreyaSyntaxError(f"Invalid flag type specified: '{s}'")


# //////////////////////////////////////////////////////////////////////////////
class HelpStr:
    def __init__(self):
        self.string = ""

    # --------------------------------------------------------------------------
    def __repr__(self):
        return self.string

    # --------------------------------------------------------------------------
    def concat(self, s: str):
        if self.string and not self.string.endswith('\n'):
            self.string += ' '
        self.string += s


# //////////////////////////////////////////////////////////////////////////////
class Rule:
    def __init__(self, raw_rule: str):
        self._raw_rule = raw_rule
        self._raw_user_value: str = ""
        self.help_str: HelpStr = HelpStr()

        self.name: str
        self.is_positional: bool
        self.is_optional: bool
        self.kw_is_optional: bool
        self.flag_short: str
        self.flag_long: str
        self.default_value: str
        self.flag_type: FlagType
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

        self.flag_type = FlagType.from_str(buffer)


    # --------------------------------------------------------------------------
    def __repr__(self):
        return f"Arg(opt={self.is_optional} posit={self.is_positional} fs={self.flag_short} fl={self.flag_long} "+\
            f"opt_kw={self.kw_is_optional} default={self.default_value} ftype={self.flag_type} nargs={self.n_args})"+\
            f"help='{self.help_str.string[:10]}'"


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
            raise FreyaSyntaxError(f"Short flags should be 1 character long, but got '{self.flag_short}'.")

        return buffer, False, flag_short, flag_long


    # --------------------------------------------------------------------------
    def _parse_n_args(self, buffer: str) -> tuple[str, bool, int]:
        if not buffer:
            if self.default_value:
                raise FreyaSyntaxError(f"Flags with no arguments can't have a default value ('{self._raw_rule}')")
            if self.is_positional:
                raise FreyaSyntaxError(f"Positional arguments must specify type and number of arguments ('{self._raw_rule}')")

            return "", False, 0

        n_args, buffer = self._assert_split_into_2(buffer, '.')
        kw_is_optional = n_args.startswith('~')

        if kw_is_optional: n_args = n_args[1:]

        if n_args == '*':
            return buffer, kw_is_optional, -1

        if not n_args.isdigit():
            raise FreyaSyntaxError(f"Invalid number of arguments specified: '{n_args}'")

        return buffer, kw_is_optional, int(n_args)


    # --------------------------------------------------------------------------
    def _assert_split_into_2(self, buffer: str, char_split: str) -> tuple[str, str]:
        splitted = buffer.split(char_split)
        if len(splitted) == 2: return splitted
        raise FreyaSyntaxError(f"Invalid substring found inside argument rule: '{self._raw_rule}'")


# //////////////////////////////////////////////////////////////////////////////
class Node:
    def __init__(self, name: str, parent: "Node|None"):
        self.name = name
        self.parent: "Node|None" = parent
        self.children: dict[str, "Node"] = {}
        self.depth = 0 if self.is_root() else parent.depth + 1
        self.rules: dict[str, Rule] = {}
        self.help_str: HelpStr = HelpStr()

    # --------------------------------------------------------------------------
    def __repr__(self):
        values = ','.join('' if v is None else str(v) for v in self.children.values())
        return f"Node({self.depth}:{self.name}){{{values if values else ''}}}"

    # --------------------------------------------------------------------------
    def __getitem__(self, name: str) -> "Node":
        return self.get_child(name)

    # --------------------------------------------------------------------------
    def add_child(self, name: str) -> "Node":
        self._assert_unique_child(name)
        child = Node(name, self)
        self.children[name] = child
        return child

    # --------------------------------------------------------------------------
    def get_child(self, name: str) -> "Node":
        if name not in self.children:
            raise FreyaSyntaxError(f"Branch '{name}' is not defined in the CLI rules.")
        return self.children[name]

    # --------------------------------------------------------------------------
    def is_root(self) -> bool: return self.parent is None
    def is_leaf(self) -> bool: return not self.children

    # --------------------------------------------------------------------------
    def _assert_unique_child(self, name: str):
        if name in self.children:
            raise FreyaSyntaxError(f"Duplicate child branch '{name}' specified inside the same branch.")


# //////////////////////////////////////////////////////////////////////////////
class FreyaParser:
    def __init__(self, raw_rules: str, raw_help: str):
        rules = self._preprocess_macros(raw_rules)
        helps = self._preprocess_macros(raw_help)

        self.tree = Node('', None)
        self.node = self.tree
        self._tree_build_rules(rules)
        self._tree_add_helps(helps)


    # --------------------------------------------------------------------------
    @classmethod
    def from_files(cls, path_fyr: str|Path, path_fyh: str|Path) -> "FreyaParser":
        return cls(
            raw_rules = Path(path_fyr).read_text(),
            raw_help = Path(path_fyh).read_text(),
        )


    # --------------------------------------------------------------------------
    def _tree_build_rules(self, rules: str):
        node: Node = self.tree
        for token in rules.split():
            if token.startswith('@'):
                name = token[1:]
                if not name: raise FreyaSyntaxError("Branch names can't be empty.")
                node = node.add_child(name)
                continue

            if token == "!@":
                if node.depth == 0: raise FreyaSyntaxError("Unexpected '!@' token found outside of any branch.")
                node = node.parent
                continue

            rule = Rule(token)
            if rule.name in node.rules:
                raise FreyaSyntaxError(f"Duplicate definition of '{rule}'.")

            node.rules[rule.name] = rule

        if not node.is_root():
            raise FreyaSyntaxError(f"Unterminated branch (missing !@ keyword {node.depth} times)")


    # --------------------------------------------------------------------------
    def _tree_add_helps(self, helps: str):
        def find_first_space(s: str) -> int:
            idx = s.find(' ')
            return len(s) if idx == -1 else idx

        node: Node = self.tree
        help_str: HelpStr = self.tree.help_str

        for row in helps.split('\n'):
            row = row.strip()

            if row.startswith('@'):
                first_space = find_first_space(row)
                name = row[1:first_space]
                if not name: raise FreyaSyntaxError("Branch names can't be empty.")

                node = node.get_child(name)
                row = row[first_space+1:].lstrip()

            elif row.startswith("!@"):
                if node.depth == 0: raise FreyaSyntaxError("Unexpected '!@' token found outside of any branch.")
                first_space = find_first_space(row)

                node = node.parent
                row = row[first_space+1:].lstrip()

            fyh_start = row.find("!fyh:")
            if fyh_start != -1:
                first_space = find_first_space(row)
                key = row[5:first_space]
                row = row[first_space+1:].lstrip()

                if key == '_':
                    help_str = node.help_str
                elif key in node.rules:
                    help_str = node.rules[key].help_str
                else:
                    raise FreyaSyntaxError(f"Help specified for non-existent rule '{key}'.")

            if not row: continue
            help_str.concat(row)


    # --------------------------------------------------------------------------
    @classmethod
    def _preprocess_macros(cls, rules: str):
        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
        def get_next_macro_idxs(s: str) -> tuple[int, int]|None:
            i0 = s.find("!def")
            if i0 == -1: return

            i1 = s.find("!fed")
            if i1 == -1: raise FreyaSyntaxError("!def macro is missing the '!fed' closure.")

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
                    raise FreyaSyntaxError("A !def macro is missing its name.")

                macro_key = macro_split[0]
                macro_val = "" if len(macro_split) == 1 \
                    else '\n'.join(macro_split[1:])

                if "!def" in macro_val:
                    raise FreyaSyntaxError("Nested !def macros are not allowed")

                if macro_key in macros:
                    raise FreyaSyntaxError(f"Duplicate definition of '{macro_key}' macro")

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
    parser = FreyaParser.from_files(dir_example / "fy_rules.fyr", dir_example / "fy_help.fyh")

    print(parser.tree.help_str, '\n')
    print(*parser.tree["smiffer"]["rna"].rules.items(), '', sep = '\n')
    print(*parser.tree["vgtools"]["convert"].rules.items(), '', sep = '\n')
    print(*parser.tree["vgtools"]["compare"].rules.items(), '', sep = '\n')


################################################################################
