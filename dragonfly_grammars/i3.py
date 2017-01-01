"""Grammar for controlling the i3 window manager."""
from aenea import (
    Grammar,
    MappingRule,
    Key,
    ProxyPlatformContext,
    Function,
    Choice,
    IntegerRef,
    Dictation)
from dragonfly_grammars.common import _, execute_keystr

class OpenProcessRule(MappingRule):

    """Rules for opening process."""

    mapping = {
        _('open terminal'): Key('w-t'),
        # TODO: treat text like basic commandline
        _('open process <text>'): Key('w-m') + Function(execute_keystr),
    }
    extras = [Dictation('text')]

def n_to_key(n):
    """Convert number to workspace keysym."""
    if n < 10:
        return n
    elif n == 10:
        return 0
    elif n == 11:
        return 'minus'
    elif n == 12:
        return 'equal'

def go_to_workspace(n):
    """Switch to workspace n."""
    Key("w-{}".format(n_to_key(n))).execute()

def move_to_workspace(n):
    """Move window to workspace n."""
    Key("sw-{}".format(n_to_key(n))).execute()

class WorkspaceRules(MappingRule):

    """Rules for movement in workspaces."""

    mapping = {
        _('workspace <n>'): Function(go_to_workspace),
        _('move [to] workspace <n>'): Function(move_to_workspace),
        _('window <direction>'): Key('w-%(direction)s'),
        _('move window [to the] <direction>'): Key('sw-%(direction)s'),
        }
    extras = [
        IntegerRef('n', 1, 13),
        Choice(
            'direction',
            {
                _('left'): 'left',
                _('right'): 'right',
                _('up'): 'up',
                _('down'): 'down'}),
        ]

GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    context = ProxyPlatformContext('linux')
    GRAMMAR = Grammar('i3', context=context)
    GRAMMAR.add_rule(OpenProcessRule())
    GRAMMAR.add_rule(WorkspaceRules())
    GRAMMAR.load()

    print 'i3 grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is not None:
        GRAMMAR.unload()
        GRAMMAR = None
