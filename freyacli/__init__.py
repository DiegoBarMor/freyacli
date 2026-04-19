from ._misc.freya_syntax_error import FreyaSyntaxError
from ._misc.arg_dtype import ArgDType

from ._utils.color import Color

from ._parsers.components.help_str import HelpStr
from ._parsers.components.argument_rule import ArgumentRule
from ._parsers.components.subcommand import Subcommand

from ._parsers.freya_parser import FreyaParser
from ._parsers.args_parser import ArgsParser

from ._core.app import App

WIDTH_TERMINAL: int = 1 # automatically set to the current terminal width when App is initialized
