import os
import click
from pathlib import Path

class TupleParam(click.ParamType):
    name: str = "tuple"

    def convert(self, value: str, param, ctx):
        if value == "all":
            return ("all",)  # "all" をタプルで返す
        try:
            parts = value.split(",")
            return tuple(parts)
        except Exception:
            self.fail(f"{value!r}は誤入力です", param, ctx)

class dir_manager:
    def __init__(self) -> None:
        self.root_path = Path(__file__).parent.parent.resolve()


    def setup_dir(self, dirname: str) -> None:
        dir_path = self.root_path / dirname
        dir_path.mkdir(exist_ok=True)

    def search_py_files(self, dirname: str) -> int:
        dir_path = self.root_path / dirname
        py_files = []
        with os.scandir(dir_path) as entries:
            for entry in entries:
                if entry.name.endswith(".py"):
                    py_files.append(entry)
        return py_files

    def print_py_file_path(self, py_file_name: str) -> None:
        py_file_path = self.root_path / py_file_name
        print(f"\t{py_file_path}")

TUPLE = TupleParam()

@click.command()
@click.option("-t", "--total", default=12, type=int, help="ファイルの総数")
@click.option("-d", "--dirnames", default="all", type=TUPLE ,help="対象ディレクトリ")
def echo_files(total: int, dirnames: tuple[str]) -> None:
    """タプルが使えるかどうかの検証 => OK"""
    if isinstance(dirnames, tuple) and len(dirnames) == 1 and dirnames[0] == "all":
        return

    for dirname in dirnames:
        dm = dir_manager()
        dm.setup_dir(dirname)
        pfs = dm.search_py_files(dirname)
        count = len(pfs)
        click.echo(f"{dirname}-dir has {count}-py-files.")
        for pf in pfs:
            pf_name = pf.name
            dm.print_py_file_path(pf_name)


if __name__ == "__main__":
    echo_files()
