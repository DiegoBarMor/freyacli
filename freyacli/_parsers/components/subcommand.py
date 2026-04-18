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
    def str_help_long(self) -> str:
        def pad_name(s: str) -> str:
            return f"    {s.ljust(max_name_len)}  - "

        if self.is_leaf():
            return "" # [TODO]

        max_name_len = max(map(len, self.children.keys()))
        width_name = len(pad_name(""))
        width_desc = max(1, fy.WIDTH_TERMINAL - width_name)

        rows_commands = '\n'.join((
            f"{pad_name(name)}{child.help_str.wrapped_text(width_name, width_desc)}"
            for name, child in self.children.items()
        ))

        return '\n'.join((
            self.help_str.nl_surround(fy.WIDTH_TERMINAL),
            "commands:",
            "  The following subcommands are available:",
            "",
            "  COMMAND",
            rows_commands,
        ))

    # --------------------------------------------------------------------------
    def _assert_unique_child(self, name: str):
        if name in self.children:
            raise fy.FreyaSyntaxError(f"Duplicate child branch '{name}' specified inside the same branch.")


# //////////////////////////////////////////////////////////////////////////////
