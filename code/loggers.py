# code/logger.py

import logging
from pathlib import Path
from code.utils import project_root

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
