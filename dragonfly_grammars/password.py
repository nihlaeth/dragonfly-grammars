#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Passwords for speech recognition.

Provide encrypted password storage.
"""
import string
from pathlib2 import Path
from simplecrypt import decrypt, DecryptionException
import natlinkstatus
from aenea import Grammar, Key, CompoundRule, ListRef, Dictation
from dragonfly import List
from dragonfly_grammars.common import _, text_to_keystr

class PasswordRule(CompoundRule):

    """Retrieve stored password."""

    def __init__(self, *args, **kwargs):
        self.spec = _("password <name> <passphrase>")
        self.names = List(name='names')
        self.data_path = Path().home().joinpath(
            'speechpass')
        self.data_path.mkdir(exist_ok=True)
        self.language_path = self.data_path.joinpath(
            natlinkstatus.NatlinkStatus().getLanguage())
        self.language_path.mkdir(exist_ok=True)
        for name in self.language_path.iterdir():
            self.names.append(string.replace(name.name, '_', ' '))
        self.extras = [
            ListRef(name='name', list=self.names),
            Dictation(name='passphrase'),
            ]

        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        name = node.get_child_by_name('name').value()
        name = string.replace(name, ' ', '_')
        password_file = self.language_path.joinpath(name)
        if not password_file.exists():
            print "file does not exist, could not decrypt password"
            return ""
        passphrase = str(node.get_child_by_name(
            'passphrase').value()).strip().lower()
        crypt_text = password_file.read_bytes()
        try:
            plaintext = decrypt(passphrase, crypt_text)
        except DecryptionException:
            print "incorrect passphrase"
            return ""
        return text_to_keystr(plaintext)

    def _process_recognition(self, node, extras):
        Key(self.value(node)).execute()


GRAMMAR = None

def load():
    """Register grammar."""
    global GRAMMAR
    GRAMMAR = Grammar('command_line_interface')
    GRAMMAR.add_rule(PasswordRule())
    GRAMMAR.load()

    print 'password grammar: Loaded.'

def unload():
    """Unregister grammar."""
    global GRAMMAR
    if GRAMMAR is None:
        GRAMMAR.unload()
        GRAMMAR = None
