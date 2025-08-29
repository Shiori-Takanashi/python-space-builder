# code/practice_checker.py

from pathlib import Path
import inspect

class PracChecker:
    def __init__(self) -> None:
        self.root_path = project_root()

    @staticmethod
    def get_error_msg(dirpath: Path) -> str:
        caller = inspect.stack()[1].function
        return f"Error: {dirpath.name}, {caller}"

    def return_about_dir(self, dirpath: Path) -> str:
        if not (dirpath.exists() and dirpath.is_dir()):
            return self.get_error_msg(dirpath)

        lst = [1 for p in dirpath.iterdir() if p.is_file() and p.suffix == ".py"]
        count = sum(lst)
        return f"{dirpath.name}({count:02d})"

    def return_pyfiles_name(self, dirpath: Path) -> str:
        if not (dirpath.exists() and dirpath.is_dir()):
            return self.get_error_msg(dirpath)

        pyfiles_name = [
            p.name for p in dirpath.iterdir() if p.is_file() and p.suffix == ".py"
        ]
        pyfiles_name_with_tab = [f"\t{p}" for p in pyfiles_name]
        return "\n".join(sorted(pyfiles_name_with_tab))
