"""Load and unload grammars and handle language setting."""
import gettext
from pkg_resources import resource_filename, Requirement
import natlinkstatus
from dragonfly_grammars.common import set_translator
import dragonfly_grammars.aenea_
import dragonfly_grammars.i3
import dragonfly_grammars.global_
gettext.bindtextdomain(
    'dragonfly_grammars',
    resource_filename(
        Requirement.parse('dragonfly_grammars'),
        'translations'))
gettext.textdomain('dragonfly_grammars')
ENX = gettext.translation('dragonfly_grammars', languages=['en'])
NLD = gettext.translation('dragonfly_grammars', languages=['nl'])
set_translator(ENX.gettext)

def load_grammars():
    """Set language, reload grammar modules and register grammars."""
    lang = natlinkstatus.NatlinkStatus().getLanguage()
    if lang == 'enx':
        set_translator(ENX.gettext)
    elif lang == 'nld':
        set_translator(NLD.gettext)
    else:
        # fallback
        set_translator(ENX.gettext)
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
