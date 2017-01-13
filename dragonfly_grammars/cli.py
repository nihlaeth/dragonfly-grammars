"""Rules for cli programs."""

from aenea import (
    Grammar,
    MappingRule,
    Key,
    Alternative,
    Choice,
    Repetition,
    RuleRef,
    CompoundRule)
from dragonfly_grammars.common import (
    _,
    extract_values,
    text_to_keystr,
    join_actions,
    Text)
from dragonfly_grammars.context import terminal_not_vim

class SshOptions(MappingRule):

    """Options for ssh."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _('[with] X forwarding'): Text('-Y')}
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
            return Text("{}@{}".format(
                user.value(), server.value()))
        return Text(server.value())


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
        return join_actions(' ', [Text('ssh')] + extract_values(
            node,
            (SshOptions, SshServer, Command),
            recurse=True))

    def _process_recognition(self, node, extras):
        self.value(node).execute()

class SudoRule(CompoundRule):

    """Superuser do commands."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = _("sudo <command>")
        self.extras = [
            RuleRef(name='command', rule=Command()),
            ]
        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        return Text('sudo ') + node.get_child_by_name(
            'command').value()

    def _process_recognition(self, node, extras):
        self.value(node).execute()

class SimpleCommand(MappingRule):

    """Commands that generally don't need arguments."""

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _("swich user"): Text("su -"),
            _("change directory"): Text("cd "),
            _("foreground"): Text("fg"),
            _("list"): Text("ls"),
            _("list all"): Text("ls -la"),
            _("remove"): Text("rm "),
            _("remove directory"): Text("rm -r "),
            _("make directory"): Text("mkdir "),
            _("move"): Text("mv "),
            _("link"): Text("ln -s "),
            _("screen"): Text("screen"),
            _("attach screen"): Text("screen -x "),
            _("disk usage"): Text("du -c -h -d1"),
            _("disc find"): Text("df -h"),
            _("service"): Text("/etc/rc.d/rc."),
            _("process grep"): Text("pgrep "),
            _("process kill"): Text("pkill -KILL"),
            _("grep"): Text("grep "),
            _("web get"): Text("wget "),
            _("secure copy"): Text("scp "),
            _("secure copy directory"): Text("scp -r "),
            _("copy"): Text("cp"),
            _("copy directory"): Text("cp -r "),
            _("(edit|vim)"): Text("vim "),
            _("touch"): Text("touch "),
            _("python"): Text("python "),
            _("H top"): Text("htop"),
            _("kill"): Text("kill -sKILL "),
            _("alsa mixer"): Text("alsamixer"),
            _("Q jack"): Text("qjackctl"),
            _("Q synth"): Text("qsynth"),
            _("H G status"): Text("hg status"),
            _("H G add"): Text("hg add "),
            _("H G commit"): Text('hg commit -m "'),
            _("H G push"): Text("hg push"),
            _("H G log"): Text("hg log"),
            _("H G diff[erence]"): Text("hg diff"),
            _("H G clone"): Text("hg clone"),
            _("scan [first]"): Text("scan"),
            _("scan second"): Text("scan2"),
            _("git status"): Text("git status"),
            _("git add"): Text("git add "),
            _("git commit"): Text('git commit -m "'),
            _("git push"): Text("git push"),
            _("git log"): Text("git log"),
            _("git diff[erence]"): Text("git diff"),
            _("git clone"): Text("git clone "),
            _("untar"): Text("tar -xvf "),
            _("telegram"): Text("Telegram"),
            _('firefox'): Text('firefox'),
            _('print working directory'): Text('pwd'),
            _('password gorilla'): Text('passwordgorilla')}
        MappingRule.__init__(self, *args, **kwargs)

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
    GRAMMAR = Grammar(
        'command_line_interface',
        context=terminal_not_vim())
    GRAMMAR.add_rule(SshRule())
    GRAMMAR.add_rule(SimpleCommand())
    GRAMMAR.add_rule(SudoRule())
    GRAMMAR.load()

    print 'cli grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
