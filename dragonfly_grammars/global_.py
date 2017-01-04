"""Grammar for commands useful in a global context."""
import string
from aenea import (
    Grammar,
    MappingRule,
    Key,
    CompoundRule,
    RuleRef,
    Alternative,
    Repetition,
    Function,
    IntegerRef,
    Dictation)
from dragonfly_grammars.common import _, execute_keystr, extract_values

class Symbol(MappingRule):

    """Symbols, brackets, whitespace and interpunction."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('(left|open) angle [bracket]'): 'langle',
            _('(left|open) [curly] brace'): 'lbrace',
            _('(left|open) [square] bracket'): 'lbracket',
            _('(left|open) paren'): 'lparen',
            _('(right|close) angle [bracket]'): 'rangle',
            _('(right|close) [curly] brace'): 'rbrace',
            _('(right|close) [square] bracket'): 'rbracket',
            _('(right|close) paren'): 'rparen',
            _('(ampersand|and)'): 'ampersand',
            _('apostrophe'): 'apostrophe',
            _('asterisk'): 'asterisk',
            _('at'): 'at',
            _('backslash'): 'backslash',
            _('backtick'): 'backtick',
            _('[vertical] bar'): 'bar',
            _('caret'): 'caret',
            _('colon'): 'colon',
            _('comma'): 'comma',
            _('dollar [sign]'): 'dollar',
            _('(dot|period|full stop)'): 'dot',
            _('double quote'): 'dquote',
            _('equal[s]'): 'equal',
            _('exclamation [point]'): 'exclamation',
            _('hash'): 'hash',
            _('hyphen'): 'hyphen',
            _('percent [sign]'): 'percent',
            _('plus [sign]'): 'plus',
            _('question[mark]'): 'question',
            _('semicolon'): 'semicolon',
            _('slash'): 'slash',
            _('tilde'): 'tilde',
            _('underscore'): 'underscore',
            _('space'): 'space',
            _('(enter|newline)'): 'enter',
            _('tab [key]'): 'tab',
        }
        MappingRule.__init__(self, *args, **kwargs)

class Number(MappingRule):

    """Numeral."""
    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('zero'): '0',
            _('one'): '1',
            _('two'): '2',
            _('three'): '3',
            _('four'): '4',
            _('five'): '5',
            _('six'): '6',
            _('seven'): '7',
            _('eight'): '8',
            _('nine'): '9',
        }
        MappingRule.__init__(self, *args, **kwargs)

class LowercaseCharacter(MappingRule):

    """Lowercase alphabetic character."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('alpha'): 'a',
            _('bravo'): 'b',
            _('charlie'): 'c',
            _('delta'): 'd',
            _('echo'): 'e',
            _('foxtrot'): 'f',
            _('golf'): 'g',
            _('hotel'): 'h',
            _('india'): 'i',
            _('juliet'): 'j',
            _('kilo'): 'k',
            _('lima'): 'l',
            _('mike'): 'm',
            _('november'): 'n',
            _('oscar'): 'o',
            _('papa'): 'p',
            _('quebec'): 'q',
            _('romeo'): 'r',
            _('sierra'): 's',
            _('tango'): 't',
            _('uniform'): 'u',
            _('victor'): 'v',
            _('whiskey'): 'w',
            _('x-ray'): 'x',
            _('yankee'): 'y',
            _('zulu'): 'z'}
        for char in string.uppercase:
            self.mapping[char] = char.lower()
        MappingRule.__init__(self, *args, **kwargs)

class UppercaseCharacter(CompoundRule):

    """Uppercase character."""

    def __init__(self, *args, **kwargs):
        self.spec = _('cap <lowercase_letter>')
        self.extras = [RuleRef(
            name='lowercase_letter',
            rule=LowercaseCharacter)]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return 's-{}'.format(extract_values(
            node, [LowercaseCharacter], recurse=True)[0])

class AnyCharacter(CompoundRule):

    """Any char."""

    def __init__(self, *args, **kwargs):
        self.spec = '<character>'
        self.extras = [Alternative(name='character', children=(
            RuleRef(rule=UppercaseCharacter),
            RuleRef(rule=LowercaseCharacter),
            RuleRef(rule=Number),
            RuleRef(rule=Symbol)))]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        # try if uppercase first, because uppercase
        # contains lowercase
        uppercase = extract_values(
            node, UppercaseCharacter, recurse=True)
        if len(uppercase) > 0:
            return uppercase[0]
        return extract_values(
            node, [LowercaseCharacter, Symbol, Number], recurse=True)[0]

class SpellingRule(CompoundRule):

    """Our very own spelling rule."""

    def __init__(self, *args, **kwargs):
        self.spec = _('spell <characters>')
        self.extras = [Repetition(
            name='characters',
            child=RuleRef(rule=AnyCharacter),
            min=1,
            max=80)]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return ','.join(extract_values(
            node, AnyCharacter, recurse=True))

class Modifier(MappingRule):

    """Modifier keys."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('control'): 'c',
            _('shift'): 's',
            _('alt'): 'a',
            _('(command|super)'): 'w'}
        MappingRule.__init__(self, *args, **kwargs)

class PressRule(CompoundRule):

    """Press keycombos."""

    def __init__(self, *args, **kwargs):
        # technically we should not accept uppercase chars here
        self.spec = _('press [<modifiers>] <character>')
        self.extras = [
            Repetition(
                name='modifiers',
                child=RuleRef(rule=Modifier),
                min=0,
                max=4),
            RuleRef(name='character', rule=AnyCharacter)]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        char = extract_values(node, AnyCharacter, recurse=True)[0]
        mods = extract_values(node, Modifier, recurse=True)
        if len(mods) == 0:
            return char
        return "{}-{}".format("".join(mods), char)

class BasicKeyboardRule(MappingRule):

    """Rules for bare keys and dictation."""

    mapping = {
        _('escape'): Key('escape'),
        _('[<n>] backspace[s]'): Key('backspace:%(n)d'),
        _('[<n>] enter[s]'): Key('enter:%(n)d'),
        _('[<n>] tab[s]'): Key('tab:%(n)d'),
        _('[<n>] space[s]'): Key('space:%(n)d'),
        _('[<n>] delete[s]'): Key('del:%(n)d'),

        _('go [<n>] up'): Key('up:%(n)d'),
        _('go [<n>] down'): Key('down:%(n)d'),
        _('go [<n>] left'): Key('left:%(n)d'),
        _('go [<n>] right'): Key('right:%(n)d'),
        _('(go home|go to start)'): Key('home'),
        _('go [to] end'): Key('end'),
        _('go [<n>] page[s] up'): Key('pgup:%(n)d'),
        _('go [<n>] page[s] down'): Key('pgdown:%(n)d'),

        _('dictate <text>'): Function(execute_keystr),
    }
    extras = [Dictation('text'), IntegerRef('n', 1, 100)]
    defaults = {
        "n": 1
    }

GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = Grammar('global')
    GRAMMAR.add_rule(BasicKeyboardRule())
    GRAMMAR.add_rule(SpellingRule())
    GRAMMAR.add_rule(PressRule())
    GRAMMAR.load()

    print 'global grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
