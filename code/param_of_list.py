# code/param_of_list.py

import click

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
