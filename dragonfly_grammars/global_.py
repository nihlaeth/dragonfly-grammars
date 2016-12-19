"""Grammar for commands useful in a global context."""
from aenea import (
    Grammar,
    MappingRule,
    Key,
    Function,
    IntegerRef,
    Dictation)
from dragonfly_grammars.text_to_key import text_to_key
from dragonfly_grammars.common import _


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

        _('dictate <text>'): Function(text_to_key),
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
    GRAMMAR.load()

    print 'global grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
