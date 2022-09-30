import curses
import operator as op
from functools import reduce

import pyfiglet
from pyfiglet import Figlet


class TextEngine:
    def __init__(self):
        self._flags = []
        self._text = ""
        self._heading = False
        self._heading_codex = dict()
        self._heading_codex[1] = "banner4"
        self._heading_codex[2] = "jazmine"
        self._heading_codex[3] = "utopia"
        self._heading_codex[4] = "marquee"
        self._heading_codex[5] = "doom"
        self._heading_codex[6] = "contessa"

    def reset(self):
        self._flags = []
        self._text = ""
        self._heading = False

    def text(self, text):
        assert isinstance(text, str), type(text)
        self._text += text

    def bold(self):
        self._flags.append(curses.A_BOLD)

    def blink(self):
        self._flags.append(curses.A_BLINK)

    def strike(self):
        self._flags.append(curses.A_REVERSE)

    def italic(self):
        self._flags.append(curses.A_ITALIC)

    def highlight(self):
        self._flags.append(curses.A_STANDOUT)

    def underline(self):
        self._flags.append(curses.A_UNDERLINE)

    def hseparator(self, scrn, cursor):
        rows, cols = scrn.getmaxyx()
        scrn.addstr(cursor.cursor_x, cursor.cursor_y, "-" * cols, curses.A_BOLD)
        cursor.next_line()

    def heading(self, level):
        self._heading = level

    def flush(self, scrn, cursor):
        if self._heading:
            self._text = pyfiglet.figlet_format(
                self._text, font=self._heading_codex[self._heading]
            )

        if len(self._flags) > 0:
            flags = reduce(op.or_, self._flags)
        else:
            flags = []

        toks = self._text.split("\n")
        for t in toks:
            args = [cursor.cursor_x, cursor.cursor_y, t]
            if flags:
                args += [flags]
            scrn.addstr(*tuple(args))
            # TODO - doesnt take into account wrapping around cursor dimensions
            cursor.forward(scrn, len(t))
            if len(toks) > 1:
                cursor.next_line()
        self.reset()
