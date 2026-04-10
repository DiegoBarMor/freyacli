import re
import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class ParserCli:
    def __init__(self, str_cli: str):
        self._str_cli = str_cli

    # --------------------------------------------------------------------------
    def parse(self):
        """
        arg_id["flag", "aliases"].TYPE 
        arg_id["flag", "aliases"].(T0|T1|T2)
        """

        def re_catch(name, pattern):
            return f"(?P<{name}>{pattern})"

        def re_variants(*patterns):
            return '|'.join(
                f"({p})" for p in patterns
            )
        
        for line in self._str_cli.splitlines():
            line = line.strip()
            if line.startswith('@'): continue # [WIP]
            if line.startswith('}'): continue
            print(f"CLI: {line}") # [WIP]

            catch_is_opt  = re_catch("is_optional", r"~?")
            catch_arg_id  = re_catch("arg_id", r"\w+")
            catch_aliases = re_catch("flag_aliases", r".*?")
            # catch_aliases = re_catch("flag_aliases", r"[^\|]*")

            variants_types = re_variants(
                r"\.\(.*\)", # multiple types
                r"\.\w+", # one type
                r"", # no types
            )
            catch_types    = re_catch("vals_types", variants_types)
            # catch_types    = re_catch("val_type", r"\w+")
            
            for x in re.finditer(rf"{catch_is_opt}{catch_arg_id}\[{catch_aliases}\]{catch_types}\s*\|?", line):
            # x = re.match(rf"\s*{re_is_opt}{re_arg_id}\[{re_aliases}\]\.{re_type}\s*", line)
                # if x is None: continue
                print("... ", end = '')
                print("§",x.group("is_optional"), end = " ")
                print("§",x.group("arg_id"), end = " ")
                print("§",x.group("flag_aliases"), end = " ")
                print("§",x.group("vals_types"), end = " ")
                print()
                print(x)
            print()


# //////////////////////////////////////////////////////////////////////////////
