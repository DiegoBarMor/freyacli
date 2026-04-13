from pathlib import Path

# //////////////////////////////////////////////////////////////////////////////
class CLIFileError(SyntaxError):
    @classmethod
    def parsing_err(cls, msg: str):
        raise CLIFileError(f"Error parsing CLI file string: {msg}")


# //////////////////////////////////////////////////////////////////////////////
class Node:
    def __init__(self, name: str, parent: "Node|None"):
        self.name = name
        self.parent: "Node|None" = parent
        self.children: dict[str, "Node"] = {}
        self.depth = 0 if parent is None else parent.depth + 1

    # --------------------------------------------------------------------------
    def __repr__(self):
        values = ','.join('' if v is None else str(v) for v in self.children.values())
        return f"Node({self.depth}:{self.name}){{{values if values else ''}}}"

    # --------------------------------------------------------------------------
    def __getitem__(self, name: str) -> "Node":
        if name not in self.children:
            CLIFileError.parsing_err(f"Argument '{name}' is not defined in the CLI rules.")
        return self.children[name]

    # --------------------------------------------------------------------------
    def add_child(self, name: str) -> "Node":
        self._assert_unique_child(name)
        child = Node(name, self)
        self.children[name] = child
        return child

    # --------------------------------------------------------------------------
    def _assert_unique_child(self, name: str):
        if name in self.children:
            CLIFileError.parsing_err(f"Duplicate argument '{name}' specified inside the same branch.")


# //////////////////////////////////////////////////////////////////////////////
class FyRulesParser:
    def __init__(self, rules: str):
        rules = self._preprocess_cli_rules(rules)
        self.tree = Node('', None)
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

            # [WIP]


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
            s = s.lower()
            while s:
                idxs = get_next_macro_idxs(s)
                if idxs is None: break
                macro_split = get_text_inside_macro(s, idxs).split()
                s = get_text_around_macro(s, idxs)

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


    # --------------------------------------------------------------------------


################################################################################
if __name__ == "__main__":
    parser = FyRulesParser.read_cli("new.cli")
    print(parser.tree)
    print(parser.tree["vgtools"]["pack"])


################################################################################
