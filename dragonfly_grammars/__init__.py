"""Load and unload grammars and handle language setting."""
import gettext
import os.path
from pkg_resources import resource_filename, Requirement
import natlinkstatus
from dragonfly_grammars.common import set_translator
from dragonfly_grammars import (
    aenea_,
    i3,
    global_,
    cli,
    vim)

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
    aenea_.load()
    i3.load()
    global_.load()
    cli.load()
    vim.load()

def unload_grammars():
    """Unregister grammars and reload grammar modules."""
    aenea_.unload()
    i3.unload()
    global_.unload()
    cli.unload()
    vim.unload()
