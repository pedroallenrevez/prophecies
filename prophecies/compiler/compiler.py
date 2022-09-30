import curses

from prophecies.parser import parse

from .cursor import Cursor
from .text_engine import TextEngine


class Compiler:
    def __init__(self):
        self.cursor = Cursor()
        self.text_engine = TextEngine()
        curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

    def __call__(self, txt):
        token = parse(txt)
        curses.wrapper(main, token)


def main(scrn, token):
    scrn.clear()
    for t in token:
        t.curses(scrn)

    scrn.refresh()
    scrn.getkey()
