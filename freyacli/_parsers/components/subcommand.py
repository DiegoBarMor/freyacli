import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class Subcomand:
    def __init__(self, name: str, parent: "Subcomand|None"):
        self.name = name
        self.parent: "Subcomand|None" = parent
        self.children: dict[str, "Subcomand"] = {}
        self.depth = 0 if self.is_root() else parent.depth + 1
        self.rules: dict[str, fy.ArgumentRule] = {}
        self.help_str: fy.HelpStr = fy.HelpStr()

    # --------------------------------------------------------------------------
    def __repr__(self):
        values = ','.join('' if v is None else str(v) for v in self.children.values())
        return f"Subcomand({self.depth}:{self.name}){{{values if values else ''}}}"

    # --------------------------------------------------------------------------
    def __getitem__(self, name: str) -> "Subcomand":
        return self.get_child(name)

    # --------------------------------------------------------------------------
    def add_child(self, name: str) -> "Subcomand":
        self._assert_unique_child(name)
        child = Subcomand(name, self)
        self.children[name] = child
        return child

    # --------------------------------------------------------------------------
    def get_child(self, name: str) -> "Subcomand":
        if name not in self.children:
            raise fy.FreyaSyntaxError(f"Branch '{name}' is not defined in the CLI rules.")
        return self.children[name]

    # --------------------------------------------------------------------------
    def is_root(self) -> bool: return self.parent is None
    def is_leaf(self) -> bool: return not self.children

    # --------------------------------------------------------------------------
    def str_help_long(self, py_name: str) -> str:
        return '\n'.join((
            self._get_usage_str(py_name),
            self.help_str.nl_surround(),
            self._get_str_leaf_arguments() if self.is_leaf() \
                else self._get_str_subcommands(),
        ))


    # --------------------------------------------------------------------------
    def _get_usage_str(self, py_name: str) -> str:
        preffix = "  " + py_name + ' '.join(self._get_path_to_root())

        usage_posits = ' '.join(
            rule._get_usage_str_positional() for rule in self._iter_rules_positional()
        )
        if usage_posits: usage_posits += ' '

        if self.is_leaf():
            ### [NOTE] options isn't currently supported for non-leaf nodes
            return f"{preffix} {usage_posits}[options...]"

        return f"{preffix} COMMAND ..."


    # --------------------------------------------------------------------------
    def _get_str_leaf_arguments(self) -> str:
        return ""


    # --------------------------------------------------------------------------
    def _get_str_subcommands(self) -> str:
        max_name_len = max(map(len, self.children.keys()))
        width_name = len(fy.HelpStr.pad_name("", max_name_len))
        width_desc = max(1, fy.WIDTH_TERMINAL - width_name)

        rows_commands = '\n'.join((
            fy.HelpStr.pad_name(name, max_name_len) +\
                child.help_str.wrapped_text(width_name, width_desc)
            for name, child in self.children.items()
        ))

        return '\n'.join((
            "commands:",
            "  The following subcommands are available:",
            "",
            "  COMMAND",
            rows_commands,
        ))


    # --------------------------------------------------------------------------
    def _get_path_to_root(self) -> list[str]:
        path = []
        node = self
        while node:
            path.append(node.name)
            node = node.parent
        return path[::-1]

    # --------------------------------------------------------------------------
    def _assert_unique_child(self, name: str):
        if name in self.children:
            raise fy.FreyaSyntaxError(f"Duplicate child branch '{name}' specified inside the same branch.")


    # --------------------------------------------------------------------------
    def _iter_rules_positional(self):
        yield from filter(lambda rule: rule.is_positional, self.rules.values())


# //////////////////////////////////////////////////////////////////////////////
