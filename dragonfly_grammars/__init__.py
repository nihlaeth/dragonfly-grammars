"""Load and unload grammars and handle language setting."""
import gettext
import os.path
from pkg_resources import resource_filename, Requirement
import natlinkstatus
from dragonfly_grammars.common import set_translator
import dragonfly_grammars.aenea_
import dragonfly_grammars.i3
import dragonfly_grammars.global_

_LOCALEDIR = os.path.join(resource_filename(
    Requirement.parse('dragonfly_grammars'),
    'dragonfly_grammars/translations'), 'language')
ENX = gettext.translation(
    'dragonfly_grammars', _LOCALEDIR, languages=['en'])
NLD = gettext.translation(
    'dragonfly_grammars', _LOCALEDIR, languages=['nl'])
set_translator(ENX.lgettext)

def load_grammars():
    """Set language, reload grammar modules and register grammars."""
    lang = natlinkstatus.NatlinkStatus().getLanguage()
    if lang == 'enx':
        set_translator(ENX.lgettext)
    elif lang == 'nld':
        set_translator(NLD.lgettext)
    else:
        # fallback
        set_translator(ENX.lgettext)
    dragonfly_grammars.aenea_ = reload(
        dragonfly_grammars.aenea_)
    dragonfly_grammars.aenea_.load()
    dragonfly_grammars.i3 = reload(dragonfly_grammars.i3)
    dragonfly_grammars.i3.load()
    dragonfly_grammars.global_ = reload(
        dragonfly_grammars.global_)
    dragonfly_grammars.global_.load()

def unload_grammars():
    """Unregister grammars and reload grammar modules."""
    dragonfly_grammars.aenea_.unload()
    dragonfly_grammars.aenea_ = reload(
        dragonfly_grammars.aenea_)
    dragonfly_grammars.i3.unload()
    dragonfly_grammars.i3 = reload(dragonfly_grammars.i3)
    dragonfly_grammars.global_.unload()
    dragonfly_grammars.global_ = reload(
        dragonfly_grammars.global_)
