import sys
from pathlib import Path
folder_root = Path(__file__).parent
folder_src = folder_root / "src"
sys.path.insert(0, str(folder_src))


import unittest

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class PrismaTuiCliTest(unittest.TestCase):
    # --------------------------------------------------------------------------
    def test_repeated_posit_names_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Posit("posit"), fy.Posit("posit")
            )
        self.assertIn("Duplicate Posit name", str(context.exception))


    # --------------------------------------------------------------------------
    def test_repeated_mode_names_ok(self):
        fy.ParserCommands(
            fy.Mode("mode", "m0"), fy.Mode("mode", "m1"),
        )


    # --------------------------------------------------------------------------
    def test_repeated_mode_aliases_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Mode("mode", "m0"), fy.Mode("mode", "m0"),
            )
        self.assertIn("Duplicate Mode alias", str(context.exception))


    # --------------------------------------------------------------------------
    def test_repeated_flag_names_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Flag("flag", "-a"), fy.Flag("flag", "-b")
            )
        self.assertIn("Duplicate Flag name", str(context.exception))


    # --------------------------------------------------------------------------
    def test_repeated_flag_aliases_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Flag("flag0", "-f"), fy.Flag("flag1", "-f")
            )
        self.assertIn("Duplicate Flag alias", str(context.exception))


    # --------------------------------------------------------------------------
    def test_repeated_kwarg_names_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Kwarg("kwarg", "-a"), fy.Kwarg("kwarg", "-b")
            )
        self.assertIn("Duplicate Kwarg name", str(context.exception))


    # --------------------------------------------------------------------------
    def test_repeated_kwarg_aliases_bad(self):
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            fy.ParserCommands(
                fy.Kwarg("kwarg0", "-k"), fy.Kwarg("kwarg1", "-k")
            )
        self.assertIn("Duplicate Kwarg alias", str(context.exception))


    # --------------------------------------------------------------------------
    def test_retrieve_unknown_flag_bad(self):
        pc = fy.ParserCommands(fy.Flag("flag", "-f"))
        with self.assertRaises(fy.PrismaTuiCliError) as context:
            _ = pc.get_flag("unknown")
        self.assertIn("Unknown Flag", str(context.exception))


    # --------------------------------------------------------------------------
    def test_retrieve_flag_and_add_help_ok(self):
        pc = fy.ParserCommands(fy.Flag("flag", "-f"))
        flag = pc.get_flag("flag")
        flag.add_help("A boolean flag")
        self.assertEqual(flag.help_str, "A boolean flag")



################################################################################
if __name__ == "__main__":
    unittest.main()


################################################################################




    # pc = fy.ParserCommands(
    #     fy.Mode("mode", "mode0").add_help("First mode of operation"),
    #     fy.Mode("mode", "mode1").add_help("Second mode of operation"),
    #     fy.Posit("posit0").add_help("First positional argument"),
    #     fy.Posit("posit1").add_help("Second positional argument"),
    #     fy.Flag("flag", "-f", "--flag").add_help("A boolean flag"),
    #     fy.Kwarg("kwarg", "-k", "--kwarg").add_help("A key-value pair argument"),
    # )

    # pc.debug()

# # argv = "src/prismatui/_cli/parser_commands.py"
# # argv = "src/prismatui/_cli/parser_commands.py posit0"
# # argv = "src/prismatui/_cli/parser_commands.py posit0 posit1"



# # argv = "src/prismatui/_cli/parser_commands.py mode posit --flag --kwarg val"

# # import sys
# # pc = ParserCommands({
# #     "verbose": {"alias": "-v", "desc": "Enable verbose output"},
# #     "debug": {"alias": "-d", "desc": "Enable debug mode"},
# #     "force": {"alias": "-f", "desc": "Force operation"},
# # })

# # pc.parse(sys.argv)

# # print("Namepy:", pc.namepy)
# # print("Posits:", pc.posits)
# # print("Modes:", pc.modes)
# # print("Flags:", pc.flags)
# # print("Kwargs:", pc.kwargs)

# # python src/prismatui/_cli/parser_commands.py mode posit --flag --kwarg val
