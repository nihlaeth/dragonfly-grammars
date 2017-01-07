"""Rules for cli programs."""

from aenea import (
    Grammar,
    MappingRule,
    Alternative,
    Choice,
    Repetition,
    #AppContext,
    #ProxyAppContext,
    RuleRef,
    CompoundRule)
from dragonfly_grammars.common import _, execute_keystr, extract_values

class SshOptions(MappingRule):

    """Options for ssh."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('[with] X forwarding'): '-Y'}
        MappingRule.__init__(self, *args, **kwargs)

class SshServer(CompoundRule):

    """User and server."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = _("[<user> at] <server>")
        self.extras = [
            Choice(
                'user',
                {_("me"): "nihlaeth"}),
            Choice(
                'server',
                {
                    _("cerridwen"): "cerridwen",
                    _("yemanja"): "yemanja",
                    _("iris"): "iris",
                    _("aine"): "aine",
                    _("dayea"): "dayea",
                    _("brighid"): "brighid",
                    _("freya"): "freya",
                    _("arthemis"): "arthemis",
                    _("morrighan"): "morrighan",
                    _("epona"): "epona",
                    _("athena"): "athena",
                    _("echo"): "echo",
                    _("hera"): "hera",
                    _("hera boot"): "heraboot",
                    _("pele"): "pele",
                    _("eileen"): "eileen",
                    _("inanna"): "inanna.humanity4all.nl",
                    _("anubis"): "anubis.humanity4all.nl",
                })]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        user = node.get_child_by_name('user', shallow=True)
        server = node.get_child_by_name('server', shallow=True)
        if user:
            return "{}@{}".format(user.value(), server.value())
        return server.value()


class SshRule(CompoundRule):

    """Most common ssh use."""

    def __init__(self, *args, **kwargs):
        self.spec = _("S S H [<ssh_options>] <server> [<command>]")
        self.extras = [
            Repetition(
                name='ssh_options',
                min=0,
                max=10,
                child=RuleRef(
                    name='ssh_option',
                    rule=SshOptions())),
            RuleRef(name='server', rule=SshServer()),
            RuleRef(name='command', rule=Command())]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return ' '.join(['ssh'] + extract_values(
            node,
            (SshOptions, SshServer, Command),
            recurse=True))

    def _process_recognition(self, node, extras):
        execute_keystr(self.value(node))

class SimpleCommand(MappingRule):

    """Commands that generally don't need arguments."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('firefox'): 'firefox',
            _('print working directory'): 'pwd',
            _('password gorilla'): 'passwordgorilla'}
        MappingRule.__init__(self, *args, **kwargs)

    def _process_recognition(self, value, extras):
        execute_keystr(value)

class Command(CompoundRule):

    """Any command except ssh for recursion reasons."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = _("command <command>")
        self.extras = [Alternative(name='command', children=(
            RuleRef(rule=SimpleCommand()),))]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return extract_values(node, (
            SimpleCommand), recurse=True)[0]


GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = Grammar('command_line_interface')
    #context=(
    #AppContext('putty') | ProxyAppContext('terminator')))
    GRAMMAR.add_rule(SshRule())
    GRAMMAR.add_rule(SimpleCommand())
    GRAMMAR.load()

    print 'global grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
