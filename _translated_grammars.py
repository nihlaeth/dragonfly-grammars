"""Load and unload dragonfly_grammars."""
import dragonfly_grammars

dragonfly_grammars.load_grammars()

def unload():
    """Unregister grammars."""
    dragonfly_grammars.unload_grammars()
