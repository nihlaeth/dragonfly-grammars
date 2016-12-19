"""Common values and functions for dragonfly_grammars."""
_GETTEXT_FUNC = lambda text: text
# pylint: disable=unnecessary-lambda
_ = lambda text: _GETTEXT_FUNC(text)

def set_translator(gettext_function):
    """Change translatorfunc (language change)."""
    global _GETTEXT_FUNC
    _GETTEXT_FUNC = gettext_function
