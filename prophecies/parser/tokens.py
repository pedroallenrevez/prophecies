from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel

import prophecies


class TagNode(BaseModel):
    content: List[Union["TagNode", str]]
    name: str
    attrs: Dict[str, Union[bool, str]]
    begin_pos: Tuple[int, int]
    end_pos: Tuple[int, int]
    _tmpl: Optional[str] = None

    class Config:
        underscore_attrs_are_private = True

    def _repr(self, level=0):
        leveled = lambda s: ("  "*level) + s
        base = leveled(f"{self.__class__.__name__}(\n")
        base += leveled(str(self.attrs) + '\n')
        for c in self.content:
            if isinstance(c, str):
                base += leveled(leveled(c + '\n'))
            else:
                base += c._repr(level=level+1) + '\n'
        base += leveled(")")
        return base

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return self._repr()

    def __init__(self, content, name, attrs, **kwargs):
        fields = self.possible_attrs()

        if attrs is not None:
            keys = list(attrs.keys())
            for k in keys:
                if k in fields:
                    kwargs[k] = attrs[k]
                    del attrs[k]
        super().__init__(content=content, name=name, attrs=attrs, **kwargs)

    def possible_attrs(self):
        keys = list(self.__class__.__dict__["__fields__"].keys())
        keys.remove("content")
        keys.remove("name")
        keys.remove("attrs")
        return keys

    def parse_template(self):
        raise NotImplementedError()

    def curses(self, scrn):
        for c in self.content:
            c.curses(scrn)


TagNode.update_forward_refs()


class Tmpl(TagNode):
    pass


class BodyToken(TagNode):
    def curses(self, scrn):
        pass
        for c in self.content:
            c.curses(scrn)


class AlnumToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        cursor = comp.cursor
        for c in self.content:
            text_engine.text(c)
        text_engine.flush(scrn, cursor)


class Paragraph(TagNode):
    # style1: bool = False
    # style2: Optional[str]

    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        cursor = comp.cursor
        for c in self.content:
            c.curses(scrn)
        cursor.next_line()


# class Script(TagNode):
#    def run(self):
#        #code = compile(self.content[0], '<string>', "eval"))
#        #eval(code)
#        pass
#
## TODO - remove this, Test component parser
# class Colored(TagNode):
#    _tmpl="""<p color="blue">This is colored</p>"""
#
#    def parse_template(self):
#        # 1. jinja template with token content
#        tmpl = self._tmpl
#        # 2. parse
#        return Tmpl(name='template', content=lexeme(values.many()).parse(tmpl), attrs={})


class EmToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.highlight()
            b.curses(scrn)


class BoldToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.bold()
            b.curses(scrn)


class BlinkToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.blink()
            b.curses(scrn)


class BreakToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        cursor = comp.cursor
        cursor.next_line()
        for b in self.content:
            b.curses(scrn)


class HorizontalToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        cursor = comp.cursor
        text_engine.hseparator(scrn, cursor)
        for b in self.content:
            b.curses(scrn)


class ItalicToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.italic()
            b.curses(scrn)


class UnderlineToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.underline()
            b.curses(scrn)


class StrikeToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.strike()
            b.curses(scrn)


class HeadingToken(TagNode):
    @property
    def _level(self):
        return int(self.name[1])

    def __hash__(self):
        return hash(tuple([self.__class__, self._level] + self.content))

    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        text_engine.heading(self._level)
        for b in self.content:
            b.curses(scrn)


class OlToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for i, b in enumerate(self.content):
            text_engine.text(f"{i}. ")
            b.curses(scrn)


class UlToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        text_engine = comp.text_engine
        for b in self.content:
            text_engine.text("*) ")
            b.curses(scrn)


class LiToken(TagNode):
    def curses(self, scrn):
        comp = prophecies.STORE.compiler
        cursor = comp.cursor
        for b in self.content:
            b.curses(scrn)
            cursor.next_line()


# TODO - move to global store
TOKENS = {
    "text": AlnumToken,
    "p": Paragraph,
    #'script': Script,
    #'colored': Colored,
    "body": BodyToken,
    "li": LiToken,
    "ol": OlToken,
    "ul": UlToken,
    "hr": HorizontalToken,
    "br": BreakToken,
    "blink": BlinkToken,
    "em": EmToken,
    "b": BoldToken,
    "i": ItalicToken,
    "u": UnderlineToken,
    "strike": StrikeToken,
    "h1": HeadingToken,
    "h2": HeadingToken,
    "h3": HeadingToken,
    "h4": HeadingToken,
    "h5": HeadingToken,
    "h6": HeadingToken,
}


class AstTokens(dict):
    pass
