import pytest

from prophecies.parser import parse
from pathlib import Path


def test_pages_parsing():
    root = Path('pages')
    for fname in root.glob('*.tui'):
        with open(fname, 'r') as fp:
            lines = fp.read().decode('utf-8')
            assert parse(lines)

def test_error_pages_parsing():
    root = Path('pages')
    for fname in root.glob('*.tui'):
        with open(fname, 'r') as fp:
            lines = fp.read().decode('utf-8')
            with pytest.raises(Exception):
                parse(lines)
