import os
from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class PathAssertion:
    # --------------------------------------------------------------------------
    @staticmethod
    def file_in(path_file: Path) -> Path | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returrns the same input `Path` object if it passes.
        """
        if not isinstance(path_file, Path): path_file = Path(path_file)

        if not path_file.exists():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' does not exist.")
        if path_file.is_dir():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' is a folder.")
        return path_file


    # --------------------------------------------------------------------------
    @staticmethod
    def file_out(path_file: Path) -> Path | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returrns the same input `Path` object if it passes.
        """
        if not isinstance(path_file, Path): path_file = Path(path_file)

        if path_file.is_dir():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' is a folder.")
        os.makedirs(path_file.parent, exist_ok = True)
        return path_file


    # --------------------------------------------------------------------------
    @staticmethod
    def dir_out(path_dir: Path) -> Path | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returrns the same input `Path` object if it passes.
        """
        if not isinstance(path_dir, Path): path_dir = Path(path_dir)

        if path_dir.is_file():
            return fy.ArgDTypeError(f"The specified folder path '{path_dir}' is a file.")
        os.makedirs(path_dir, exist_ok = True)
        return path_dir


# //////////////////////////////////////////////////////////////////////////////
