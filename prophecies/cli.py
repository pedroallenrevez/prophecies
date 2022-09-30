import pprint as pp

import click

from prophecies import STORE, destroy_engine, init_engine
from prophecies.parser import parse as _parse


@click.command()
@click.argument("filename")
def parse(filename):
    """Check the DOM tree generated by parsing a .tui file."""
    if filename.endswith(".tui"):
        with open(filename, "rb") as fp:
            lines = fp.read().decode("utf-8")
        token = _parse(lines)
        for t in token:
            print(pp.pformat(t.dict()))
    else:
        print("Provide a file with .tui extension")


@click.command()
@click.argument("filename")
def compile(filename):
    """Compile a .tui file into a curses application."""
    if filename.endswith(".tui"):
        init_engine()
        with open(filename, "rb") as fp:
            lines = fp.read().decode("utf-8")
        STORE.compiler(lines)
        destroy_engine()
    else:
        print("Provide a file with .tui extension")


# @click.command()
# def test():
#    for i, p in enumerate(Path('tests/pages').glob('*')):
#        with open(p, 'r') as fp:
#            try:
#                init_engine()
#                lines = fp.read()
#                res = parse(lines)
#                flag = "OK"
#                STORE.compiler(lines)
#            except Exception as e:
#                destroy_engine()
#                flag = "ERROR"
#            total_chars = 88 - len(str(p)) - len(str(i)) - 2
#            print(f"={i}={p}{'='*total_chars} " + flag)
#            fp.close()


@click.group()
def default():
    pass


def make_cli():
    default.add_command(compile)
    # default.add_command(test)
    default.add_command(parse)
    default()
