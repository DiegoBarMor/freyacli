# //////////////////////////////////////////////////////////////////////////////
class HelpStr:
    def __init__(self, string: str = ""):
        self.string = string

    # --------------------------------------------------------------------------
    def __repr__(self):
        return self.string

    # --------------------------------------------------------------------------
    def concat(self, s: str):
        if self.string and not self.string.endswith('\n'):
            self.string += ' '
        self.string += s

    # --------------------------------------------------------------------------
    def wrapped_text(self, indent: int, width: int) -> str:
        out = ""
        buffer = self.string.replace('\n', ' ')
        while buffer:
            if len(buffer) > width:
                row = buffer[:width]
                last_space = row[::-1].find(' ') + 1
                idx = len(row) - last_space
            else:
                idx = len(buffer)

            if out: out += f"\n{indent*' '}"
            out += buffer[:idx]
            buffer = buffer[idx+1:]

        return out

    # --------------------------------------------------------------------------
    def nl_surround(self, width: int) -> str:
        if not self.string: return self.string
        return f"\n{self.wrapped_text(0, width)}\n"


# //////////////////////////////////////////////////////////////////////////////
