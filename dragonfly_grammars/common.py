"""Common values and functions for dragonfly_grammars."""
import string
from aenea import Key

_GETTEXT_FUNC = lambda text: text
# pylint: disable=unnecessary-lambda
_ = lambda text: _GETTEXT_FUNC(text)

def set_translator(gettext_function):
    """Change translatorfunc (language change)."""
    global _GETTEXT_FUNC
    _GETTEXT_FUNC = gettext_function

def extract_values(node, types, recurse=False):
    """Return list of values from children matching types."""
    matches = []
    for child in node.children:
        if isinstance(child.actor, types):
            matches.append(child.value())
        if recurse:
            matches.extend(extract_values(child, types, True))
    return matches

def text_to_keystr(text):
    """Translate string to keynames for Key."""
    if text is None:
        return None
    charnames = {
        '<': 'langle',
        '{': 'lbrace',
        '[': 'lbracket',
        '(': 'lparen',
        '>': 'rangle',
        '}': 'rbrace',
        ']': 'rbracket',
        ')': 'rparen',
        '&': 'ampersand',
        "'": 'apostrophe',
        '*': 'asterisk',
        '@': 'at',
        '\\': 'backslash',
        '`': 'backtick',
        '|': 'bar',
        '^': 'caret',
        ':': 'colon',
        ',': 'comma',
        '$': 'dollar',
        '.': 'dot',
        '"': 'dquote',
        '=': 'equal',
        '!': 'exclamation',
        '#': 'hash',
        '-': 'hyphen',
        '%': 'percent',
        '+': 'plus',
        '?': 'question',
        ';': 'semicolon',
        '/': 'slash',
        '~': 'tilde',
        '_': 'underscore',
        ' ': 'space',
        '\n': 'enter',
        '\r\n': 'enter',
        '\t': 'tab',
    }
    for character in string.lowercase + string.digits:
        charnames[character] = character
    for character in string.uppercase:
        charnames[character] = 's-{}'.format(character)
    return ','.join(
        [charnames[character] for character in str(text)])

class Text(Key):

    """
    Text object that works with any Xdo version.
    """

    def _parse_spec(self, spec):
        Key._parse_spec(
            self,
            text_to_keystr(spec))


def execute_keystr(text):
    """Type out text."""
    Key(text_to_keystr(text)).execute()
