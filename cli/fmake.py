import os
import click
from pathlib import Path
from typing import Iterable, Iterator


# --- ユーティリティ ---

def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()


def convert_dirname_to_dirpath(dirname: str | Path) -> Path:
    """相対ディレクトリ名（または Path）から絶対 Path を作る。"""
    root = project_root()
    return root / dirname


# --- Click ParamType ---

class TupleParam(click.ParamType):
    """'a,b,c' → (Path(...), ...) / 'all' / 'none' を解釈。"""
    name: str = "tuple"

    def get_dirs(self) -> tuple[Path, ...]:
        """プロジェクト直下のディレクトリを全件返す。"""
        root = project_root()
        return tuple(p for p in root.iterdir() if p.is_dir())

    def get_dirs_endswith_s(self) -> tuple[Path, ...]:
        """プロジェクト直下で末尾が 's' のディレクトリを全件返す。"""
        root = project_root()
        # glob("*") でも可。引数なしの glob() は誤り。
        return tuple(p for p in root.iterdir() if p.is_dir() and p.name.endswith("s"))

    def convert(self, value: str, param, ctx):
        v = value.strip()  # 両端だけ
        if v.lower() == "none":
            return None
        if v.lower() == "all":
            return self.get_dirs_endswith_s()

        try:
            # 各トークンにも strip、かつ空要素は除外
            parts = tuple(p for p in (s.strip() for s in v.split(",")) if p)
            if not parts:
                return None

            exists_dirs = set(self.get_dirs())  # Path の集合（O(1) 判定）
            paths = tuple(
                path for name in parts
                if (path := convert_dirname_to_dirpath(name)) in exists_dirs
            )
            return paths
        except Exception:
            self.fail(f"{value!r}は誤入力です", param, ctx)


# --- 主要クラス ---

class FileChecker:
    def __init__(self) -> None:
        self.root_path = project_root()
        self.py_files_path = None

    def search_py_files(self, dirname: str | Path) -> list[Path]:
        """指定ディレクトリ内の .py ファイル一覧を Path で返す。"""
        dir_path = convert_dirname_to_dirpath(dirname)
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        self.py_files_path = [p for p in dir_path.iterdir() if p.is_file() and p.suffix == ".py"]
        return self.py_files_path

    def print_py_file_path(self, py_file: Path) -> None:
        py_file_path = self.root_path / py_file
        print(f"\t{py_file_path}")

class FileMaker:
    def __init__(self) -> None:
        self.root_path = project_root()

    def setup_dir(self, dirname: str | Path) -> None:
        dir_path = convert_dirname_to_dirpath(dirname)
        dir_path.mkdir(exist_ok=True)



TUPLE = TupleParam()


# --- 分岐 ---

def check_files(dirnames: tuple[Path, ...] | None) -> None:
    """タプルが使えるかどうかの検証 => OK"""
    if dirnames is None:
        return

    fc = FileChecker()
    for dirname in dirnames:
        py_files = fc.search_py_files(dirname)
        count = len(py_files)
        click.echo(f"{dirname.name}-dir has {count}-py-files.")
        for pf in py_files:
            fc.print_py_file_path(pf)

    return

def make_files(total: int, dirnames: tuple[Path, ...] | None) -> None:
    return



# --- CLI ---

@click.command()
@click.option("-t", "--total", default=12, type=int, help="ファイルの総数")
@click.option("-d", "--dirnames", default="none", type=TUPLE, help="対象ディレクトリ")
@click.option("-c", "--check", is_flag=True, help="確認モードかどうか。")
def run(total: int, dirnames: tuple[Path, ...] | None, check: bool) -> None:
    if check:
        check_files(dirnames)
    else:
        make_files(total, dirnames)
    return


if __name__ == "__main__":
    run()
