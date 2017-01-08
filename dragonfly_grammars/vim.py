#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vim grammar.

Rules for everything vim and vim-like. Actually consists
of multiple grammars for context purposes.

TODO: marks, symbols and digits, repetition, window mode
"""

from aenea import (
    MappingRule,
    CompoundRule,
    RuleRef,
    Choice,
    Repetition,
    Key)

from dragonfly_grammars.common import _, extract_values
from dragonfly_grammars.global_ import Number

MOTION_OPERATORS = (
    ('change', 'c'),
    ('delete', 'd'),
    ('yank', 'y'),
    ('swap case', 'g,tilde'),
    ('make lowercase', 'g,u'),
    ('make uppercase', 'g,s-u'),
    ('filter', 'exclamation'),
    ('C filter', 'equal'),
    ('text formatting', 'g,q'),
    ('rotation 13 encoding', 'g,question'),
    ('shift right', 'rangle'),
    ('shift left', 'langle'),
    ('define fold', 'z,f'),
    ('call function', 'g,at'),
    )

class MotionRule(MappingRule):

    """Motion commands."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            ################
            #  left/right  #
            ################
            _("left"): "h",
            _("right"): "l",
            _("(zero|first char)"): "zero",
            _("(caret|first non-blank char)"): "caret",
            _("(dollar|last char)"): "dollar",
            _("last visible non-blank char"): "g,underscore",
            _("fist visible char"): "g,zero",
            _("first visible non-blank char"): "g,caret",
            _("middle of line"): "g,m",
            _("last visible char"): "g,dollar",
            _("(pipe|to column)"): "bar",
            # _("find <char>"): "f",
            # _("backwards find <char>"): "s-f",
            #############
            #  up/down  #
            #############
            _("up"): "k",
            _("down"): "j",
            _("visible up"): "g,k",
            _("visible down"): "g,j",
            _("(minus|linewise non-blank up)"): "minus",
            _("(plus|linewise non-blank down)"): "plus",
            _("(underscore|down to first non-blank)"): "underscore",
            _("goto"): "s-g",
            _("end of [last] line"): "c-end",
            _("first non-blank char of [first] line"): "g,g",
            _("percent"): "percent",
            ##########
            #  word  #
            ##########
            _("word"): "w",
            _("(big|cap) word"): "s-w",
            _("end"): "e",
            _("(big|cap) end"): "s-e",
            _("back"): "b",
            _("(big|cap) back"): "s-b",
            _("backward end"): "g,e",
            _("backward (big|cap) end"): "g,s-e",
            #################
            #  text object  #
            #################
            _("((open|left) paren|sentence backward)"): "lparen",
            _("((close|right) paren|sentence forward)"): "rparen",
            _("((left|open) curly brace|paragraph backward)"): "lbrace",
            _("((right|close) curly brace|paragraph forward"): "rbrace",
            _("next section start"): "rbracket,rbracket",
            _("next section end"): "rbracket,lbracket",
            _("previous section start"): "lbracket,rbracket",
            _("previous section end"): "lbracket,lbracket",
            ###########
            #  other  #
            ###########
            _("ex"): "colon",
            }

        MappingRule.__init__(self, *args, **kwargs)

class VisualMotionRule(MappingRule):

    """
    Motion commands wich are only valid in visual modes and after operators.
    """

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _("a word"): "a,w",
            _("inner word"): "i,w",
            _("a (big|cap) word"): "a,s-w",
            _("inner (big|cap) word"): "i,s-w",
            _("a sentence"): "a,s",
            _("inner sentence"): "i,s",
            _("a paragraph"): "a,p",
            _("inner paragraph"): "i,p",
            _("a bracket block"): "a,lbracket",
            _("inner bracket block"): "i,lbracket",
            _("a paren block"): "a,b",
            _("inner paren block"): "i,b",
            _("an angle block"): "a,langle",
            _("inner angle block"): "i,langle",
            _("a tag block"): "a,t",
            _("inner tag block"): "i,t",
            _("a curly block"): "a,s-b",
            _("inner curly block"): "i,s-b",
            _("a quoted string"): "a,dquote",
            _("inner quoted string"): "i,dquote",
            }

        MappingRule.__init__(self, *args, **kwargs)

class MotionOperatorRule(CompoundRule):

    """Commands with motion component."""

    exported = False
    _motion_cmd = _('delete')
    _motion_char = 'd'

    def __init__(self, *args, **kwargs):
        self.spec = _(
            "{} [<numbers>] (<motion>|<operatormotion>) [into buffer <buffer>] [<mode> mode]").format(
                self._motion_cmd)
        self.extras = [
            Repetition(
                name='numbers',
                child=RuleRef(rule=Number()),
                min=0,
                max=3),
            RuleRef(name='motion', rule=MotionRule()),
            RuleRef(name='operatormotion', rule=VisualMotionRule()),
            Choice(name='buffer', choices={
                _("default"): "$",
                }),
            Choice(name='mode', choices={
                _("character"): "v",
                _("line"): "s-v",
                _("block"): "c-v",
                })
            ]

        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        cmd_elements = []

        ######################################
        #  buffer to place affected text in  #
        ######################################
        if node.has_child_with_name('buffer'):
            cmd_elements.append("dquote")
            cmd_elements.append(
                node.get_child_by_name('buffer').value())

        #####################
        #  motion operator  #
        #####################
        cmd_elements.append(self._motion_char)

        ##########
        #  mode  #
        ##########
        # overwrites operator's default mode
        # think blockwise, linewise, charwise
        if node.has_child_with_name('mode'):
            cmd_elements.append(
                node.get_child_by_name('mode').value())

        ##########################
        #  numerator for motion  #
        ##########################
        # is multiplied with any numbers preceding
        # this command by vim
        cmd_elements.extend(extract_values(node, Number, recurse=True))

        ###################
        #  actual motion  #
        ###################
        # think w
        if node.has_child_with_name('motion'):
            cmd_elements.append(
                node.get_child_by_name('motion').value())
        if node.has_child_with_name('operatormotion'):
            cmd_elements.append(
                node.get_child_by_name(
                    'operatormotion').value())

        return ','.join(cmd_elements)

    def _process_recognition(self, node, extras):
        Key(self.value(node)).execute()

class VimNormalRule(MappingRule):

    """Commands for vim normal mode."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            _("addition"): "c-a",
            _("scroll back screen"): "c-b",
            _("interrupt"): "c-c",
            _("scroll down half"): "c-d",
            _("scroll extra up"): "c-e",
            _("scroll forward screen"): "c-f",
            _("display file name"): "c-g",
            _("redraw screen"): "c-l",
            _("jumplist newer"): "c-i",
            _("jumplist older"): "c-o",
            _("redo"): "c-r",
            _("tag older"): "c-t",
            _("scroll half up"): "c-u",
            _("visual block"): "c-v",
            _("window"): "c-w",
            _("subtract"): "c-x",
            _("scroll down"): "c-y",
            _("suspend"): "c-z",
            _("insertmode"): "c-backslash,c-g",
            _("indent"): "c-rbracket",
            _("edit alternate"): "c-caret",
            _("cap append"): "s-a",
            _("copy to end of line"): "s-c",
            _("delete to end of line"): "s-d",
            _("find char left"): "s-f",
            _("goto line from top of screen"): "s-h",
            _("insert at start of line"): "s-i",
            _("join lines"): "s-j",
            _("lookup keyword"): "s-k",
            _("goto line from bottom of screen"): "s-l",
            _("goto middle of screen"): "s-m",
            _("backwards next"): "s-n",
            _("insert on newline before"): "s-o",
            _("paste before"): "s-p",
            _("external mode"): "s-q",
            _("replace mode"): "s-r",
            _("switch lines"): "s-s",
            _("backwards move to char"): "s-t",
            _("undo on line"): "s-u",
            _("visual line"): "s-v",
            _("backwards delete char"): "s-x",
            _("yank line"): "s-y",
            _("store and exit"): "s-z,s-z",
            _("unsafe exit"): "s-z,s-q",
            _("append"): "a",
            _("(insert|inner)"): "i",
            }

        MappingRule.__init__(self, *args, **kwargs)
