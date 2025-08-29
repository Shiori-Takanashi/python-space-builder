import inspect
import logging
from pathlib import Path

import click

# --- ユーティリティ ---


def project_root() -> Path:
    return Path(__file__).parent.parent.resolve()


def convert_dirname_to_dirpath(dirname: str) -> Path:
    """相対ディレクトリ名（または Path）から絶対 Path を作る。"""
    root = project_root()
    return root / dirname


# --- ロガー ---
def count_logfile(logs_dirpath: Path) -> int:
    """既存の .log ファイル数をカウントして次の番号を返す。"""
    count = 0
    for file in logs_dirpath.glob("*.log"):
        count += 1
    return count + 1


def get_loggers() -> logging.Logger:
    """
    ロギング設定。
    標準出力とファイル両方に INFO レベルで出力する。
    """
    # loggerを設定
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # --- フォーマッタ ---
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )

    # --- 標準ハンドラ ---
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # --- ファイルハンドラ ---
    rootpath = project_root()
    logs_dirpath = rootpath / "logs"
    logs_dirpath.mkdir(exist_ok=True)

    log_number = count_logfile(logs_dirpath)
    logs_filename = f"prac_build{log_number:03d}.log"
    logs_filepath = logs_dirpath / logs_filename

    file_handler = logging.FileHandler(logs_filepath, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # --- ハンドラを登録 ---
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


# --- Click ParamType ---


class ListParam(click.ParamType):
    """clickをカスタムするためのクラス"""

    name: str = "list"

    def get_dirnames_endswith_prac(self) -> list[str]:
        """root直下の_pracで終わるディレクトリ名を返却"""
        root = project_root()
        return [
            p.name for p in root.iterdir() if p.is_dir() and p.name.endswith("_prac")
        ]

    def convert(self, value: str, param, ctx):
        v = value.strip()
        if v.lower() == "none":
            return []
        if v.lower() == "all":
            return self.get_dirnames_endswith_prac()
        try:
            # stripは必須
            dirnames: list = sorted(p for p in (s.strip() for s in v.split(",")))
            if not dirnames:
                return []
            return dirnames
        except Exception:
            self.fail(f"{value!r}は誤入力です", param, ctx)


# --- 主要クラス ---


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


LIST = ListParam()


@click.command()
@click.option("-t", "--total", default=3, type=int, help="ファイルの総数")
@click.option("-d", "--dirnames", default="none", type=LIST, help="対象ディレクトリ")
@click.option("-c", "--check", is_flag=True, help="確認モードかどうか。")
def run(total: int, dirnames: list[str] | None, check: bool) -> None:
    dirnames_with_prac = [d + "_prac" for d in dirnames]
    dirpaths = sorted(
        convert_dirname_to_dirpath(dirname_with_prac)
        for dirname_with_prac in dirnames_with_prac
    )

    pc = PracChecker()

    for dirpath in dirpaths:
        msg_about_dir = pc.return_about_dir(dirpath)
        msg_about_pyfiles = pc.return_pyfiles_name(dirpath)

        msg = "\n".join([msg_about_dir, msg_about_pyfiles])
        click.echo(msg)


if __name__ == "__main__":
    run()
