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
    def __call__(self, uvs: fy.UserValues) -> list[fy.UserValues]:
        """
        Asserts `Path` values inside a `fy.UserValues` instance.
        Returns a list of found errors, if any, wrapped inside the faulty `fy.UserValues` instances.
        An empty `fy.UserValues` isn't considered an error (though this should never happen when assertions are called in `fy.App`).
        An empty list is returned when no errors are found.
        """
        if self == self.NO_ASSERTION:      func = lambda _: None
        if self == PathAssertion.FILE_IN:  func = self._assert_file_in
        if self == PathAssertion.FILE_OUT: func = self._assert_file_out
        if self == PathAssertion.DIR_OUT:  func = self._assert_dir_out
        return list(filter(
            None, (func(obj_path) for obj_path in uvs.get_paths())
        ))


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_file_in(cls, path_file: Path) -> fy.UserValues | None:
        if not path_file.exists():
            return fy.UserValues.init_wrong(f"The specified file path '{path_file}' does not exist.")
        if path_file.is_dir():
            return fy.UserValues.init_wrong(f"The specified file path '{path_file}' is a folder.")


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_file_out(cls, path_file: Path) -> fy.UserValues | None:
        if path_file.is_dir():
            return fy.UserValues.init_wrong(f"The specified file path '{path_file}' is a folder.")
        os.makedirs(path_file.parent, exist_ok = True)


    # --------------------------------------------------------------------------
    @classmethod
    def _assert_dir_out(cls, path_dir: Path) -> fy.UserValues | None:
        if path_dir.is_file():
            return fy.UserValues.init_wrong(f"The specified folder path '{path_dir}' is a file.")
        os.makedirs(path_dir, exist_ok = True)


# //////////////////////////////////////////////////////////////////////////////
