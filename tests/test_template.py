#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test template formats."""

import textwrap
import pytest

from pygments.lexers import Angular2HtmlLexer
from pygments.token import Token

@pytest.fixture(scope='module')
def lexer_ng2():
    yield Angular2HtmlLexer()


def testAngularFragment(lexer_ng2):
    # Not starting with v makes this test work (remove the first token  from
    # tokens in that case)
    fragment = 'v*39j5Sq='
    tokens = [
        (Token.Text, 'v'),
        (Token.Punctuation, '*'),
        (Token.Name.Attribute, '39j5Sq'),
        (Token.Operator, '='),
        (Token.Text, '\n')
    ]
    assert list(lexer_ng2.get_tokens(fragment)) == tokens