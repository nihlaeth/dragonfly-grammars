"""Grammar for controlling the i3 window manager."""
from aenea import (
    Grammar,
    MappingRule,
    Key,
    Function,
    Choice,
    IntegerRef,
    RuleRef)
from dragonfly_grammars.common import _
from dragonfly_grammars.context import linux
from dragonfly_grammars.cli import Command

class OpenProcessRule(MappingRule):

    """Rules for opening process."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('open terminal'): Key('w-t'),
            _('open process [<cmd>]'): Key('w-m,%(cmd)s')
        }
        self.extras = [
            RuleRef(name='cmd', rule=Command())]
        MappingRule.__init__(self, *args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('workspace <n>'): Function(go_to_workspace),
            _('move [to] workspace <n>'): Function(move_to_workspace),
            _('window <direction>'): Key('w-%(direction)s'),
            _('move window [to the] <direction>'): Key('sw-%(direction)s'),
            }
        self.extras = [
            IntegerRef('n', 1, 13),
            Choice(
                'direction',
                {
                    _('left'): 'left',
                    _('right'): 'right',
                    _('up'): 'up',
                    _('down'): 'down'}),
            ]
        MappingRule.__init__(self, *args, **kwargs)

GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = Grammar('i3', context=linux())
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
