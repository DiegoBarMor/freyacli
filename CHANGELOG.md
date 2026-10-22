# Changelog

## [0.5.0] - 2026-10-22
- Refactored the handling of user-provided values.
    - Introduced the `UserValues` class.
- Cleaned up the App *argument getter* and *path assertion* methods.
- Removed `ANY` flag type.
    - `STR` type shold be considered as the default generic type for values provided via CLI.


## [0.4.5] - 2026-10-18
- Bugfix in path assertion.
- Bugfix in `-h` flag usage.


## [0.4.4] - 2026-06-24
- Improved the help message when insufficient values are provided for a flag.
- Added `ANY` flag type.
    - It parses values like a `STR` type.
    - Its purpose is to show in the help string that a flag receives values with potentially different types (e.g. either a number or a path).
    - Its value(s) should be retrieved with `get_arg_str`.
    - Any necessary parsing should be done afterwards.


## [0.4.3] - 2026-05-28
- Fixed bug when parsing quoted numeric argument lists.
- Improved `freyacli summary`.
    - Subcommands are now properly sorted according to their order of occurrence inside the FYR file.
    - Summary is now formatted as a markdown table.


## [0.4.2] - 2026-05-21
- Fixed bug where path assertion wasn't returning the potential errors generated during the assertion.


## [0.4.1] - 2026-05-05
- Fixed bug related to the new path assertion.


## [0.4.0] - 2026-05-01
- Reworked the App getter and path assertion methods.


## [0.3.2] - 2026-04-29
- Improved how the application name is displayed in the usage string.


## [0.3.1] - 2026-04-26
- Fixed bug with bad recognition of negative values as argument.


## [0.3.0] - 2026-04-24
- `freyacli` package now contains an integrated freyacli application.
    - If the package is installed, the application will be accessible with the command `freyacli`.
    - It will provide utilities relevant when dealing with freyacli apps.


## [0.2.0] - 2026-04-22
- Fixed several bugs.
- Improved the public interface for the `App` class.


## [0.1.1] - 2026-04-21
- Fixed issue with colors in environments without terminal.


## [0.1.0] - 2026-04-20
- Initial upload to PyPI.
