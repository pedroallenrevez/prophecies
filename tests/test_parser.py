from prophecies.parser import parse

def test_parse_paragraph():
    res = parse("<p>lala<p>asdfas</p></p>")
    assert res

def test_parse_paragraph_spaces():
    res = parse("<p >lala <p   >a .  sdfas</p></p>")
    assert res

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
    assert res

