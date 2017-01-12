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
    IntegerRef,
    Dictation)
from dragonfly_grammars.common import _, extract_values, Text

class Symbol(MappingRule):

    """Symbols, brackets, whitespace and interpunction."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('(left|open) angle [bracket]'): Key('langle'),
            _('(left|open) [curly] brace'): Key('lbrace'),
            _('(left|open) [square] bracket'): Key('lbracket'),
            _('(left|open) paren'): Key('lparen'),
            _('(right|close) angle [bracket]'): Key('rangle'),
            _('(right|close) [curly] brace'): Key('rbrace'),
            _('(right|close) [square] bracket'): Key('rbracket'),
            _('(right|close) paren'): Key('rparen'),
            _('(ampersand|and)'): Key('ampersand'),
            _('apostrophe'): Key('apostrophe'),
            _('asterisk'): Key('asterisk'),
            _('at'): Key('at'),
            _('backslash'): Key('backslash'),
            _('backtick'): Key('backtick'),
            _('[vertical] bar'): Key('bar'),
            _('caret'): Key('caret'),
            _('colon'): Key('colon'),
            _('comma'): Key('comma'),
            _('dollar [sign]'): Key('dollar'),
            _('(dot|period|full stop)'): Key('dot'),
            _('double quote'): Key('dquote'),
            _('equal[s]'): Key('equal'),
            _('exclamation [point]'): Key('exclamation'),
            _('hash'): Key('hash'),
            _('hyphen'): Key('hyphen'),
            _('percent [sign]'): Key('percent'),
            _('plus [sign]'): Key('plus'),
            _('question[mark]'): Key('question'),
            _('semicolon'): Key('semicolon'),
            _('slash'): Key('slash'),
            _('tilde'): Key('tilde'),
            _('underscore'): Key('underscore'),
            _('space'): Key('space'),
            _('(enter|newline)'): Key('enter'),
            _('tab [key]'): Key('tab'),
        }
        MappingRule.__init__(self, *args, **kwargs)

class Number(MappingRule):

    """Numeral."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('zero'): Key('0'),
            _('one'): Key('1'),
            _('two'): Key('2'),
            _('three'): Key('3'),
            _('four'): Key('4'),
            _('five'): Key('5'),
            _('six'): Key('6'),
            _('seven'): Key('7'),
            _('eight'): Key('8'),
            _('nine'): Key('9'),
        }
        MappingRule.__init__(self, *args, **kwargs)

class LowercaseCharacter(MappingRule):

    """Lowercase alphabetic character."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('alpha'): Key('a'),
            _('bravo'): Key('b'),
            _('charlie'): Key('c'),
            _('delta'): Key('d'),
            _('echo'): Key('e'),
            _('foxtrot'): Key('f'),
            _('golf'): Key('g'),
            _('hotel'): Key('h'),
            _('india'): Key('i'),
            _('juliet'): Key('j'),
            _('kilo'): Key('k'),
            _('lima'): Key('l'),
            _('mike'): Key('m'),
            _('november'): Key('n'),
            _('oscar'): Key('o'),
            _('papa'): Key('p'),
            _('quebec'): Key('q'),
            _('romeo'): Key('r'),
            _('sierra'): Key('s'),
            _('tango'): Key('t'),
            _('uniform'): Key('u'),
            _('victor'): Key('v'),
            _('whiskey'): Key('w'),
            _('x-ray'): Key('x'),
            _('yankee'): Key('y'),
            _('zulu'): 'z'}
        for char in string.uppercase:
            self.mapping[char] = char.lower()
        MappingRule.__init__(self, *args, **kwargs)

class UppercaseCharacter(CompoundRule):

    """Uppercase character."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = _('cap <lowercase_letter>')
        self.extras = [RuleRef(
            name='lowercase_letter',
            rule=LowercaseCharacter())]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return 's-{}'.format(extract_values(
            node, LowercaseCharacter, recurse=True)[0])

class AnyCharacter(CompoundRule):

    """Any char."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = '<character>'
        self.extras = [Alternative(name='character', children=(
            RuleRef(rule=UppercaseCharacter()),
            RuleRef(rule=LowercaseCharacter()),
            RuleRef(rule=Number()),
            RuleRef(rule=Symbol())))]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        # try if uppercase first, because uppercase
        # contains lowercase
        uppercase = extract_values(
            node, UppercaseCharacter, recurse=True)
        if len(uppercase) > 0:
            return uppercase[0]
        return extract_values(
            node, (LowercaseCharacter, Symbol, Number), recurse=True)[0]

class SpellingRule(CompoundRule):

    """Our very own spelling rule."""

    def __init__(self, *args, **kwargs):
        self.spec = _('spell <characters>')
        self.extras = [Repetition(
            name='characters',
            child=RuleRef(rule=AnyCharacter()),
            min=1,
            max=80)]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return sum(extract_values(
            node, AnyCharacter, recurse=True))

    def _process_recognition(self, node, extras):
        self.value(node).execute()

class Modifier(MappingRule):

    """Modifier keys."""
    # TODO: return action objects instead of plain strings

    exported = False

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
                child=RuleRef(rule=Modifier()),
                min=0,
                max=4),
            RuleRef(name='character', rule=AnyCharacter())]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        char = extract_values(node, AnyCharacter, recurse=True)[0]
        mods = extract_values(node, Modifier, recurse=True)
        if len(mods) == 0:
            return char
        return Key("{}-{}".format("".join(mods), str(char)))

    def _process_recognition(self, node, extras):
        self.value(node).execute()

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

        _('dictate <text>'): Text('%(text)s'),
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
