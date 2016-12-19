"""Send strings via Key."""
import string
from aenea import Key

def text_to_key(text):  # type: text: NatlinkDictationContainer -> None
    """Send text with Key."""
    charnames = {
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
    Key(','.join(
        [charnames[character] for character in str(text)])).execute()
