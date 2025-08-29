from pathlib import Path


class PathManager:
    def __init__(self, input_dirnames: list[str]) -> None:
        self.rootpath = Path(__file__).parent.parent.resolve()
        self.input_dirnames = input_dirnames
        self.dirpaths: list[Path] | None = None

    def get_dirpath(self):
        for dirname in self.input_dirnames:
            if not isinstance(dirname, str):
                raise
            dirpath = self.rootpath / dirname
            yield dirpath

    def get_dirpaths(self) -> list[Path]:
        self.dirpaths = [self.rootpath / dirname for dirname in self.input_dirnames]
