from prophecies.parser import parse
from prophecies.parser.tokens import Paragraph, AlnumToken

def test_parse_paragraph():
    res = parse("<p>lala<p>asdfas</p></p>")
    assert res
    assert isinstance(res[0], Paragraph)
    assert isinstance(res[0].content[0], AlnumToken)
    assert res[0].content[0].content[0] == "lala"
    assert isinstance(res[0].content[1], Paragraph)
    assert isinstance(res[0].content[1].content[0], AlnumToken)
    assert res[0].content[1].content[0].content[0] == "asdfas"

def test_parse_paragraph_spaces():
    res = parse("<p >lala<p   >asdfas</ p></p  >")
    assert res
    assert isinstance(res[0], Paragraph)
    assert isinstance(res[0].content[0], AlnumToken)
    assert res[0].content[0].content[0] == "lala"
    assert isinstance(res[0].content[1], Paragraph)
    assert isinstance(res[0].content[1].content[0], AlnumToken)
    assert res[0].content[1].content[0].content[0] == "asdfas"

def test_parse_attrs():
    s = """<p>
        b
        <p style1>
            aaaa
            <p style2="yoyoyo">
            </p>
            a
        </p>
    </p>
    """
    res = parse(s)
    print(res)
    assert res
    second_p = res[0].content[1]
    assert "style1" in second_p.attrs
    assert second_p.attrs['style1'] == True
    third_p = second_p.content[1]
    assert "style2" in third_p.attrs
    assert third_p.attrs['style2'] == "yoyoyo"

