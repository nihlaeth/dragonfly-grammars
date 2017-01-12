"""Grammar for controlling the i3 window manager."""
from aenea import (
    Grammar,
    MappingRule,
    CompoundRule,
    Key,
    Function,
    Choice,
    Alternative,
    IntegerRef,
    RuleRef)
from dragonfly_grammars.common import _
from dragonfly_grammars.context import linux
from dragonfly_grammars.cli import Command, SshRule

class OpenProcessRule(CompoundRule):

    """Rules for opening process."""

    def __init__(self, *args, **kwargs):
        self.spec = _('open process [<cmd>]')
        self.extras = [
            Alternative(name='cmd', children=(
                RuleRef(name='ssh', rule=SshRule()),
                RuleRef(name='command', rule=Command()),
                )),]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        cmd = Key('w-m')
        if node.has_child_with_name('ssh'):
            cmd += node.get_child_by_name('ssh').value()
        elif node.has_child_with_name('command'):
            cmd += node.get_child_by_name('command').value()
        return cmd

    def _process_recognition(self, node, extras):
        self.value(node).execute()

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
            _('open terminal'): Key('w-t'),
            _('workspace <n>'): Function(go_to_workspace),
            _('move [to] workspace <n>'): Function(move_to_workspace),
            _('window <direction>'): Key('w-%(direction)s'),
            _('move window [to the] <direction>'): Key('sw-%(direction)s'),
            _("fullscreen"): Key("w-f"),
            _("tabbed layout"): Key("w-w"),
            _("tiling layout"): Key("w-e"),
            _("stacking layout"): Key("w-s"),
            _("kill focused window"): Key("ws-q"),
            _("horizontal split"): Key("w-h"),
            _("vertical split"): Key("w-v"),
            _("toggle floating"): Key("ws-space"),
            _("focus floating"): Key("w-space"),
            _("reload i3 config file"): Key("ws-c"),
            _("restart i3 in place"): Key("ws-r"),
            _("I'm really sure I want to exit i3"): Key("ws-e"),
            _("resize mode"): Key("w-r"),
            _("invert screen rotation"): Key("ws-a"),
            _("reset screen rotation"): Key("ws-n"),
            _("(display|show) window info"): Key("ws-t"),
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
