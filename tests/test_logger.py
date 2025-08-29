# tests/test_logger.py
import logging
from pathlib import Path

import pytest
from code import loggers as logger_mod

def test_count_logfile(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    # 既存なし → 1を返す
    assert logger_mod.count_logfile(logs) == 1
    # ダミー .log を3つ作成 → 次は4
    for i in range(3):
        (logs / f"dummy{i}.log").write_text("", encoding="utf-8")
    assert logger_mod.count_logfile(logs) == 4


def test_get_loggers_writes_stdout_and_file(tmp_path: Path, monkeypatch, caplog):
    # project_root() を一時ディレクトリに差し替え
    monkeypatch.setattr(logger_mod, "project_root", lambda: tmp_path)

    # pytest のログキャプチャ
    caplog.set_level(logging.INFO)

    logger = logger_mod.get_loggers()
    logger.info("hello-world")

    # 標準出力へ出ているか（caplog 経由）
    assert "hello-world" in caplog.text

    # ファイルへ出ているか
    logs_dir = tmp_path / "logs"
    log_files = list(logs_dir.glob("prac_build*.log"))
    assert len(log_files) == 1, "ログファイルが1つ生成されているはず"
    text = log_files[0].read_text(encoding="utf-8")
    assert "hello-world" in text

    # 後始末（ハンドラ二重登録回避）
    for h in logger.handlers:
        try:
            h.flush()
            h.close()
        except Exception:
            pass
    logger.handlers.clear()
