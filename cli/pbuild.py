import os
import click
from pathlib import Path
from typing import Iterable, Iterator


# --- ユーティリティ ---

def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()


def convert_dirname_to_dirpath(dirname: str) -> Path:
    """相対ディレクトリ名（または Path）から絶対 Path を作る。"""
    root = project_root()
    return root / dirname


# --- Click ParamType ---

class TupleParam(click.ParamType):
    """'a,b,c' → (Path(...), ...) / 'all' / 'none' を解釈。"""
    name: str = "tuple"


    def get_dirs_endswith_s(self) -> tuple[Path, ...]:
        """プロジェクト直下で末尾が 's' のディレクトリを全件返す。"""
        root = project_root()
        # glob("*") でも可。引数なしの glob() は誤り。
        return tuple(p for p in root.iterdir() if p.is_dir() and p.name.endswith("_prac"))

    def convert(self, value: str, param, ctx):
        v = value.strip()  # 両端だけ
        if v.lower() == "none":
            return None
        # if v.lower() == "all":
        #     return self.get_dirs_endswith_s()

        try:
            # 各トークンにも strip、かつ空要素は除外
            dirnames: list = sorted(p for p in (s.strip() for s in v.split(",")))

            if not dirnames:
                return None

            return dirnames

        except Exception:
            self.fail(f"{value!r}は誤入力です", param, ctx)


# --- 主要クラス ---

class PracChecker:
    def __init__(self) -> None:
        self.root_path = project_root()

    def return_about_dir(self, dirpath: Path) -> str:
        if not (dirpath.exists() and dirpath.is_dir()):
            return f"ERROR: {dirpath.name}"

        count = 0
        for p in dirpath.iterdir():
            if p.is_file() and p.suffix == ".py":
                count += 1
        msg = f"{dirpath.name}({count:02d})"
        return msg

    def return_pyfiles_name(self, dirpath: Path) -> str:
        if not (dirpath.exists() and dirpath.is_dir()):
            return ""
        pyfiles_name = [p.name for p in dirpath.iterdir() if p.is_file() and p.suffix ==  ".py"]
        pyfiles_name_with_tab = [f"\t{p}" for p in pyfiles_name]
        msgs = sorted(pyfiles_name_with_tab)
        if msgs:
            msg = "\n".join(msgs)
        return msg

    def check(self, dirsnames: Iterable[Path]) -> list[str]:
        return [""]

    def search_py_files(self, dir_path: Path) -> list[Path]:
        """指定ディレクトリ内の .py ファイル一覧を Path で返す。"""
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        py_file_paths =  sorted([p for p in dir_path.iterdir() if p.is_file() and p.suffix == ".py"])
        return py_file_paths

    def print_py_file_path(self, py_file_path: Path) -> None:
        print(f"  >>>  {py_file_path.name}")
        return

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

TUPLE = TupleParam()


# --- 分岐 ---

def check_files(dir_paths: tuple[Path, ...] | None) -> None:
    """タプルが使えるかどうかの検証 => OK"""
    if dir_paths is None:
        return

    fc = FileChecker()

    click.echo("====== RESULT ======")

    for dir_path in dir_paths:
        py_files = fc.search_py_files(dir_path)
        count = len(py_files)
        click.echo(f"{dir_path.name}-DIR: {count:02d}-files")
        for pf in py_files:
            fc.print_py_file_path(pf)
    return

def make_files(total: int, dir_paths: tuple[Path, ...] | None) -> None:
    if dir_paths is None:
        return

    pb = PracBuilder()

    click.echo("====== DIR    ======")

    dir_msgs = []
    for dirname in dir_paths:
        msg = pb.setup_dir(dirname)
        dir_msgs.append(msg)

    for dir_msg in dir_msgs:
        click.echo(dir_msg)

    click.echo("====== INIT   ======")

    init_msgs = []
    for dir_path in dir_paths:
        msg = pb.setup_init_file(dir_path)
        init_msgs.append(msg)

    for init_msg in init_msgs:
        click.echo(init_msg)

    click.echo("====== FILE   ======")

    file_msgs = []
    for dirname in dir_paths:
        msgs = pb.make_py_files_in_total(dirname, total)
        file_msgs.extend(msgs)

    for file_msg in file_msgs:
        click.echo(file_msg)

    return

# --- CLI ---

@click.command()
@click.option("-t", "--total", default=3, type=int, help="ファイルの総数")
@click.option("-d", "--dirnames", default="none", type=TUPLE, help="対象ディレクトリ")
@click.option("-c", "--check", is_flag=True, help="確認モードかどうか。")
def run(total: int, dirnames: list[Path, ...] | None, check: bool) -> None:
    # if check:
    #     check_files(dir_paths)
    # else:
    #     make_files(total, dir_paths)
    #     check_files(dir_paths)
    # return
    dirnames_with_prac = [d + "_prac" for d in dirnames]
    dirpaths = sorted(convert_dirname_to_dirpath(dirname_with_prac) for dirname_with_prac in dirnames_with_prac)

    pc = PracChecker()

    for dirpath in dirpaths:
        msg_about_dir = pc.return_about_dir(dirpath)
        msg_about_pyfiles = pc.return_pyfiles_name(dirpath)

        msg = "\n".join([msg_about_dir, msg_about_pyfiles])
        click.echo(msg)

if __name__ == "__main__":
    run()

# trigger: dirnamesをdir_pathsとして適した変数名に変更？
# => 変更できてない。ディレクトリ名を絶対パスに変更するポイントに違和感。
