# FREYA CLI
**Freya CLI** (FRamEwork for pYthon Applications) is, as the name suggests, a Python framework for building Command Line Interface (CLI) applications. It allows developers to use a set of well defined rules and specifications for the intended usage of the CLI (via the `FYR` format), while giving an intuitive idea to the users on how the app's CLI expects to receive.

As a bonus, **Freya CLI** provides a simple utility for coloring any printed text, via the `freyacli.Color` class. The colors provided are black, white, red, green, blue, yellow, magenta, cyan; with their respective *bright* variations, for a total of 16 colors.

## FYR / FYH format
- `FYR` (FreYa Rules) specifies a list of **rules** that must be followed when using an application's CLI. These rules are organized inside a hierarchy structure composed of **subcommand** nodes.
- `FYH` (FreYa Helps) should follow the same structure as its respective `FYR`. Instead of specifying the CLI rules, it stores the help strings that will be displayed whenever an incorrect use of the CLI is detected.

Below is an explanation of the argument **rules** and the **subcommand** nodes.

### Argument Rules
...

### Subcommands
...

## Current limitations (TODO)
- Default values shouldn't have spaces or newlines inside
- Flag --help/-h is currently reserved.
- Positional arguments / options (flags) aren't currently supported for non-leaf **subcommand** nodes.
- Execution of the app must currently happen at a leaf **subcommand** node.
