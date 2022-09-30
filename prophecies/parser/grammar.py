import operator as op
from dataclasses import dataclass
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple, Union

from parsy import generate, peek, regex, seq, string, string_from
from pydantic import BaseModel

from prophecies.parser.tokens import TOKENS

lexeme = lambda p: p << whitespace

whitespace = regex(r"[\s\\t\\n]*")
alnum = regex(r"[0-9a-zA-Z_!?\-:\s]")

number = lexeme(regex(r"-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?")).map(float)

LTAG = lexeme(string("<"))
RTAG = lexeme(string(">"))
SLASH = lexeme(string("/"))
CLTAG = LTAG + SLASH

no_tag_text_no_equal = regex(r'[^"=\\<>\s]+')


@generate
def no_tag_text():
    bp, content, ep = yield regex(r'[^"\\<>]+').mark()

    return TOKENS["text"](
        name="text", content=[content], attrs={}, begin_pos=bp, end_pos=ep
    )


# TODO - should be text no punkt
@generate
def bool_value():
    key = yield no_tag_text_no_equal
    return (key, True)


@generate
def key_value():
    key = yield no_tag_text_no_equal
    yield string("=")
    yield string('"')
    val = yield no_tag_text_no_equal
    yield string('"')
    return (key, val)


ATTR = key_value | bool_value
ATTRS = ATTR.sep_by(string(" ")).map(dict)

OPEN_TAG = lambda x: LTAG + lexeme(string(x)) >> ATTRS.optional() << RTAG
CLOS_TAG = lambda x: CLTAG + lexeme(string(x)) + RTAG
# TODO - SINGLE TAGS


def tagger(char):
    @generate
    def tag():
        # 1. Parse tag
        otag_begin_pos, attrs, otag_end_pos = (
            yield OPEN_TAG(char).desc(f"<{char}>").mark()
        )
        ctag_begin_pos, content, ctag_end_pos = yield values.many().mark()
        etag_begin_pos, _, etag_end_pos = yield CLOS_TAG(char).desc(f"</{char}>").mark()

        # 2. Produce Tokens
        token = TOKENS[char](
            name=char,
            content=content,
            attrs=attrs,
            begin_pos=otag_begin_pos,
            end_pos=etag_end_pos,
        )
        # 3. parse template - return another node
        # component node - parsed node
        if token._tmpl:
            token = token.parse_template()
        return token

    return tag


TAGS = reduce(op.or_, [tagger(k) for k in TOKENS.keys()])
# TAGS = tagger('p') | tagger('script') | tagger('colored')
values = TAGS | no_tag_text.desc("alnum text")
ROOT = values
