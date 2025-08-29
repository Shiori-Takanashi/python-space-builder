import click

from code.logger import get_loggers
from code.param_of_list import ListParam
from code.practice_buidler import PracBuilder
from code.practice_checker import PracChecker
from code.path_manager import PathManager

LIST = ListParam()


@click.command()
@click.option("-t", "--total", default=3, type=int, help="ファイルの総数")
@click.option("-d", "--dirnames", default="none", type=LIST, help="対象ディレクトリ")
@click.option("-c", "--check", is_flag=True, help="確認モードかどうか。")
def run(total: int, dirnames: list[str] | None, check: bool) -> None:
    p_manager = PathManager()
    p_manager.load(dirnames)

    # pc = PracChecker()

    # for dirpath in dirpaths:
    #     msg_about_dir = pc.return_about_dir(dirpath)
    #     msg_about_pyfiles = pc.return_pyfiles_name(dirpath)

    #     msg = "\n".join([msg_about_dir, msg_about_pyfiles])
    #     click.echo(msg)


if __name__ == "__main__":
    run()
