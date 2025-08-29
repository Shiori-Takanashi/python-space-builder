# Python-Practice-Space-Builder

Python の学習環境を構築するためのリポジトリです。
本プロジェクトでは、CLI ツールやコード整形・静的解析ツールなどを導入し、学習を効率化することを目的としています。
（作業進行中：2025/08/29）

## 使用技術

### Click
- Python 製 CLI ツールを構築するためのライブラリ。
- 環境構築の一環として導入。

### uv
- パッケージ管理ツール。
- `uv init` を用いたプロジェクト初期化から開始。

### Ruff
- Linter / Formatter。
- Black / Flake8 / isort の機能を包括するため採用。

### pyproject.toml
- Python プロジェクト設定ファイル。
- Ruff などのツール設定を一元管理するために利用。
