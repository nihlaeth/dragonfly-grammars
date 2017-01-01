"""Rules for cli programs."""

from aenea import (
    Grammar,
    MappingRule,
    Choice,
    Repetition,
    RuleRef,
    CompoundRule)
from dragonfly_grammars.common import _, execute_keystr

class SshOptions(MappingRule):

    """Options for ssh."""

    mapping = {
        _('[with] X forwarding'): '-Y'}

class SshServer(CompoundRule):

    """User and server."""

    Spec = _("[<user> at] <server>")
    extras = [
        Choice(
            'user',
            {_("me"): "nihlaeth"}),
        Choice(
            'server',
            {
                _("yemanja"): "yemanja",
                _("iris"): "iris",
                _("aine"): "aine",
            })]

class SshRule(CompoundRule):

    """Most common ssh use."""

    spec = _("S S H [<ssh_options>] <server> [<command>]")
    extras = [
        Repetition(
            'ssh_options',
            min=0,
            max=10,
            name=RuleRef(
                'ssh_option', rule=SshOptions())),
        Choice('server', {}),
        Choice('command', {})]

    def _process_recognition(self, node, extras):
        cmd = "ssh"
        if extras['ssh_options'] is not None:
            cmd = ' '.join([cmd] + extras['ssh_options'])
        cmd = "{} {}".format(cmd, extras['server'])
        if extras['command'] is not None:
            cmd = "{} {}".format(cmd, extras['command'])
        execute_keystr(cmd)

GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = Grammar('command_line_interface')
    GRAMMAR.add_rule(SshRule())
    GRAMMAR.load()

    print 'global grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
