import os
from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class PathAssertion:
    # --------------------------------------------------------------------------
    @classmethod
    def file_in(cls, path_file: Path | None, allow_none: bool = False) -> Path | None | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returns the same input `Path` object if it passes.
        If path is `None` and `allow_none` is `True`, it returns `None`.
        """
        if allow_none and path_file is None: return None
        path_file = cls._assert_path_type(path_file)
        if isinstance(path_file, fy.ArgDTypeError): return path_file

        if not path_file.exists():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' does not exist.")
        if path_file.is_dir():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' is a folder.")
        return path_file


    # --------------------------------------------------------------------------
    @classmethod
    def file_out(cls, path_file: Path | None, allow_none: bool = False) -> Path | None | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returns the same input `Path` object if it passes.
        If path is `None` and `allow_none` is `True`, it returns `None`.
        """
        if allow_none and path_file is None: return None
        path_file = cls._assert_path_type(path_file)
        if isinstance(path_file, fy.ArgDTypeError): return path_file

        if path_file.is_dir():
            return fy.ArgDTypeError(f"The specified file path '{path_file}' is a folder.")
        os.makedirs(path_file.parent, exist_ok = True)
        return path_file


    # --------------------------------------------------------------------------
    @classmethod
    def dir_out(cls, path_dir: Path | None, allow_none: bool = False) -> Path | None | fy.ArgDTypeError:
        """
        Returns an error message wrapped inside an `fy.ArgDTypeError` instance if the assertion fails.
        Returns the same input `Path` object if it passes.
        If path is `None` and `allow_none` is `True`, it returns `None`.
        """
        if allow_none and path_dir is None: return None
        path_dir = cls._assert_path_type(path_dir)
        if isinstance(path_dir, fy.ArgDTypeError): return path_dir

        if path_dir.is_file():
            return fy.ArgDTypeError(f"The specified folder path '{path_dir}' is a file.")
        os.makedirs(path_dir, exist_ok = True)
        return path_dir


    # --------------------------------------------------------------------------
    @staticmethod
    def _assert_path_type(path):
        if not isinstance(path, Path):
            try: path = Path(path)
            except TypeError: return fy.ArgDTypeError(f"The specified path '{path}' is not a valid path.")
        return path


# //////////////////////////////////////////////////////////////////////////////
