# FREYACLI
...

## FYR / FYH format
- `FYR` (FreYa Rules) specifies a list of **rules** that must be followed when using an application's CLI. These rules are organized inside a hierarchy structure composed of **subcommand** nodes.
- `FYH` (FreYa Helps) should follow the same structure as its respective `FYR`. Instead of specifying the CLI rules, it stores the help strings that will be displayed whenever an incorrect use of the CLI is detected.

Below is an explanation of the argument **rules** and the **subcommand** nodes.

### Argument Rules
...

### Subcommands
...

## Current limitations (TODO)
- Default value strings shouldn't have spaces or newlines inside
- Flag --help/-h is currently reserved.
- Positional arguments / options (flags) aren't currently supported for non-leaf **subcommand** nodes.
- Execution of the app must currently happen at a leaf **subcommand** node.
