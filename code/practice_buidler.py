# code/practice_builder.py

from pathlib import Path
import inspect

class PracBuilder:
    def __init__(self) -> None:
        self.root_path = project_root()

    def setup_dir(self, dir_path: Path) -> str:
        if dir_path.exists():
            msg = f"{dir_path.name}-DIR exists."
            return msg
        if not dir_path.exists():
            dir_path.mkdir()
            msg = f"{dir_path.name}-DIR is created."
            return msg

    def setup_init_file(self, dir_path: Path) -> str:
        init_file_path = dir_path / "__init__.py"
        if init_file_path.exists():
            msg = f"init.py in {dir_path.name} exists."
        else:
            init_file_path.touch()
            msg = f"__init__.py in {dir_path.name} is created."
        return msg

    def make_py_files_in_total(self, dir_path: Path, total: int) -> list[str]:
        dir_name = dir_path.name
        msgs = []
        for count in range(total):
            idx = count + 1
            file_path = dir_path / f"{dir_name}{idx:02d}.py"
            if file_path.exists():
                msg = f"{file_path.name} exists."
                msgs.append(msg)
            else:
                file_path.touch()
                msg = f"{file_path.name} is created."
                msgs.append(msg)
        return msgs
