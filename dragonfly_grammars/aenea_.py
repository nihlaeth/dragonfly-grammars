"""Grammar for controlling aenea."""
# This is a command module for Dragonfly. It provides support for several of
# Aenea's built-in capabilities. This module is NOT required for Aenea to
# work correctly, but it is strongly recommended.

# This file is part of Aenea
#
# Aenea is free software: you can redistribute it and/or modify it under
# the terms of version 3 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# Aenea is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Aenea.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (2014) Alex Roper
# Alex Roper <alex@aroper.net>

import dragonfly

try:
    import aenea
    import aenea.proxy_contexts
    import aenea.configuration
    import aenea.communications
    import aenea.config
    import aenea.configuration
except ImportError:
    print 'Unable to import Aenea client-side modules.'
    raise

class DisableRule(dragonfly.CompoundRule):

    """Disable remote."""

    spec = _('disable proxy server')

    def _process_recognition(self, _node, _extras):
        aenea.config.disable_proxy()


class EnableRule(dragonfly.CompoundRule):

    """Enable remote."""

    spec = _('enable proxy server')

    def _process_recognition(self, _node, _extras):
        aenea.config.enable_proxy()

SERVER_LIST = dragonfly.DictList('aenea servers')
SERVER_LIST_WATCHER = aenea.configuration.ConfigWatcher(
    ('grammar_config', 'aenea'))

class ChangeServer(dragonfly.CompoundRule):

    """Change to different remote."""

    spec = _('set proxy server to <proxy>')
    extras = [dragonfly.DictListRef('proxy', SERVER_LIST)]

    def _process_recognition(self, _node, extras):
        aenea.communications.set_server_address((
            extras['proxy']['host'],
            extras['proxy']['port']))

    def _process_begin(self):
        if SERVER_LIST_WATCHER.refresh():
            SERVER_LIST.clear()
            for k, value in SERVER_LIST_WATCHER.conf.get(
                    'servers', {}).iteritems():
                SERVER_LIST[str(k)] = value

GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = dragonfly.Grammar('aenea')

    GRAMMAR.add_rule(EnableRule())
    GRAMMAR.add_rule(DisableRule())
    GRAMMAR.add_rule(ChangeServer())

    GRAMMAR.load()

    print 'Aenea client-side modules loaded successfully'
    print 'Settings:'
    print '\tHOST:', aenea.config.DEFAULT_SERVER_ADDRESS[0]
    print '\tPORT:', aenea.config.DEFAULT_SERVER_ADDRESS[1]
    print '\tPLATFORM:', aenea.config.PLATFORM
    print '\tUSE_MULTIPLE_ACTIONS:', aenea.config.USE_MULTIPLE_ACTIONS
    print '\tSCREEN_RESOLUTION:', aenea.config.SCREEN_RESOLUTION

    try:
        aenea.proxy_contexts._get_context()
        print 'Aenea: Successfully connected to server.'
    except Exception:
        print 'Aenea: Unable to connect to server.'


def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
