# FREYA CLI
**Freya CLI** (FRamEwork for pYthon Applications) is, as the name suggests, a Python framework for building Command Line Interface (CLI) applications. It allows developers to use a set of well defined rules and specifications for the intended usage of the CLI (via the `FYR` format), while giving an intuitive idea to the users on how the app's CLI expects to receive.

As a bonus, **Freya CLI** provides a simple utility for coloring any printed text, via the `freyacli.Color` class. The colors provided are black, white, red, green, blue, yellow, magenta, cyan; with their respective *bright* variations, for a total of 16 colors.

## FYR / FYH format
- `FYR` (FreYa Rules) specifies a list of **rules** that must be followed when using an application's CLI. These rules are organized inside a hierarchy structure composed of **subcommand** nodes.
- `FYH` (FreYa Helps) should follow the same structure as its respective `FYR`. Instead of specifying the CLI rules, it stores the help strings that will be displayed whenever an incorrect use of the CLI is detected.

Below is an explanation of the argument **rules** and the **subcommand** nodes.

### Argument Rules
Argument rules specify how the arguments should be passed to the CLI, and are specified in the `FYR` format. The simplest rule has the form:
```
name[]1.STR
```
where `name` is both the name that will be used to fetch the user values, and the name displayed in the automatic help string. The empty brackets represent that this argument is **positional** (e.g. like how the argument is passed to the command `cat README.md`). The expected type is passed after a `.`, in this case `STR` (`1` indicates that one value is expected, more on that [later](#argument-count)). Supported types are:
- `STR`: string
- `PATH`: Python `Path` instance
- `INT`: integer
- `FLOAT`: float


If the argument is intended to be a simple on/off flag instead (e.g. `-a` in `ls -a`), it would instead look like
```
name[a,all]
```

This means that the flag `name` can be toggled on by passing either the flag `-a` (short name) or `--all` (long name). Short names can only be 1-character long; numbers are currently not allowed. If only a short name is to be defined, you can write it as `[a,]`; if only a long name is needed instead, it can be written as `[,all]`.

Naturally, toggle flags should be optional by nature. To indicate that an argument is **optional**, a `~``char should be placed in front of the name. This applies to any kind of argument, be it positional or flags. So the previous example would be:

```
~name[a,all]
```

Flags can also have a value attached to them. It will look similar to the positional argument syntax, with the added short/long flag names inside the brackets, e.g.:
```
~path_file[i,input]1.PATH
```

Finally, default values can be specified inside the `FYR` too. These will be assigned to optional arguments that the user didn't specify. It uses a `=` at the end of the rule (limitation: spaces are not allowed inside default values), e.g.:
```
~path_file[i,input]1.PATH=README.md
```

#### Argument Count
...

### Subcommands
...

### Macros
...

### Help String
...

## Current limitations (TODO)
- Default values shouldn't have spaces or newlines inside
- Flag --help/-h is currently reserved.
- Positional arguments / options (flags) aren't currently supported for non-leaf **subcommand** nodes.
- Execution of the app must currently happen at a leaf **subcommand** node.
- Short flag names should not be a digit. Otherwise the parser will confuse it as a float value (e.g. `-3`).
