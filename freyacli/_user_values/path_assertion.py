import os
from enum import Enum, auto
from pathlib import Path

import freyacli as fy

# //////////////////////////////////////////////////////////////////////////////
class PathAssertion(Enum):
    FILE_IN  = auto()
    FILE_OUT = auto()
    DIR_OUT  = auto()
    NO_ASSERTION = auto()

    # --------------------------------------------------------------------------
    def __call__(self, uvs: fy.UserValue, allow_empty: bool = False) -> list[fy.UserValue]:
        """
        Asserts `Path` values inside a `fy.UserValue` instance.
        Returns a list of found errors, if any, wrapped inside the faulty `fy.UserValue` instances.
        An empty `fy.UserValue` is considered an error, unless `allow_empty` is `True`.
        An empty list is returned when no errors are found.
        """
        if uvs.is_empty():
            if allow_empty: return []
            return [fy.UserValue.init_wrong("Expected at least one path.")]

        if self == self.NO_ASSERTION:      func = lambda _: None
        if self == PathAssertion.FILE_IN:  func = self._assert_file_in
        if self == PathAssertion.FILE_OUT: func = self._assert_file_out
        if self == PathAssertion.DIR_OUT:  func = self._assert_dir_out
        return list(filter(
            None, (func(obj_path) for obj_path in uvs.get_paths())
        ))


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_file_in(cls, path_file: Path) -> fy.UserValue | None:
        if not path_file.exists():
            return fy.UserValue.init_wrong(f"The specified file path '{path_file}' does not exist.")
        if path_file.is_dir():
            return fy.UserValue.init_wrong(f"The specified file path '{path_file}' is a folder.")


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_file_out(cls, path_file: Path) -> fy.UserValue | None:
        if path_file.is_dir():
            return fy.UserValue.init_wrong(f"The specified file path '{path_file}' is a folder.")
        os.makedirs(path_file.parent, exist_ok = True)


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_dir_out(cls, path_dir: Path) -> fy.UserValue | None:
        if path_dir.is_file():
            return fy.UserValue.init_wrong(f"The specified folder path '{path_dir}' is a file.")
        os.makedirs(path_dir, exist_ok = True)


# //////////////////////////////////////////////////////////////////////////////
