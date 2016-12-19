"""Load and unload grammars and handle language setting."""
import gettext
from pkg_resources import resource_filename, Requirement
import natlinkstatus
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
ENX.install()

def load_grammars():
    """Set language, reload grammar modules and register grammars."""
    lang = natlinkstatus.NatlinkStatus().getLanguage()
    if lang == 'enx':
        ENX.install()
    elif lang == 'nld':
        NLD.install()
    else:
        # fallback
        ENX.install()
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
