# dragonfly-grammars
My personal dragonfly grammars

I need my grammars to detect which language the current profile uses, and translate the grammars accordingly. So I decided to make that happen.

## Notes
I dislike the way natlink, dragonfly and aenea operate. Don't get ma wrong, they are amazing tools. But they don't make for good or elegant code. I attempted to right some of the things that bother me most in this module (mostly regarding statefullness, mucking about in system, poorly documented config files and code-reuse), but it is still a highly statefull machine.

I attempted to use built-in Python tools as much as possible. I use gettext for translations, setuptools for installation and the built-in reload for refreshing modules after a language change, or when natlink finds it necessary to reload the code. It is compatible with existing tools, but it works slightly different.

Still, it is not nearly as pythonic as I would like and I might one day get my grammars to the point where contributing to the existing tools and improving them will be easy. Right now though, all my energy is going into the grammars themselves.

## Installation
* install natlink, dragonfly & aenea
* compile translations with ```python ./setup.py compile_catalog```
* install this with pip
* move _translated_grammars.py to MacroSystem directory

## Extension

### Adding grammars
Make sure your grammars have load and unload functions, and edit __init__.py to have them called. Also make sure your grammar is reloaded there at the appropiate time.

### Adding languages
Add your language in __init__.py and have it activated in load_grammars. Then make translations with setup.py.

### Translations
Note: watch out with init_catalog, it will overwrite existing .po files
```
python ./setup.py extract-messages
python ./setup.py (init|update)_catalog --locale=<locale>
# edit relevant .po file in dragonfly_grammars/translations/language
python ./setup.py compile_catalog
```
