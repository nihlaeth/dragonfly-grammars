#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vim grammar.

Rules for everything vim and vim-like. Actually consists
of multiple grammars for context purposes.

TODO: window mode, :commands, rest of normal keybindings, filters
    other modes, vi-like mode, pentadactyl bindings, plugins, dutch translations
"""

from aenea import (
    Grammar,
    MappingRule,
    CompoundRule,
    RuleRef,
    Literal,
    Choice,
    Alternative,
    Repetition,
    Key)

from dragonfly_grammars.common import _, extract_values
from dragonfly_grammars.context import vim_normal_mode
from dragonfly_grammars.global_ import Number, AnyCharacter

##################################
#  Rules with multiple purposes  #
##################################

class MotionRule(MappingRule):

    """Motion commands."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.mapping = {
            ################
            #  left/right  #
            ################
            _("(backward|left)"): "h",
            _("(forward|right)"): "l",
            _("(zero|first char[acter])"): "0",
            _("(caret|first non-blank char[acter])"): "caret",
            _("(dollar|last char[acter])"): "dollar",
            _("last visible non-blank char[acter]"): "g,underscore",
            _("fist visible char[acter]"): "g,0",
            _("first visible non-blank char[acter]"): "g,caret",
            _("middle of line"): "g,m",
            _("last visible char[acter]"): "g,dollar",
            _("(pipe|column)"): "bar",
            _("find <char>"): "f,%(char)s",
            _("backwards find <char>"): "s-f,%(char)s",
            #############
            #  up/down  #
            #############
            _("up"): "k",
            _("down"): "j",
            _("visible up"): "g,k",
            _("visible down"): "g,j",
            _("(minus|linewise non-blank up)"): "minus",
            _("(plus|linewise non-blank down)"): "plus",
            _("(underscore|first non-blank line down)"): "underscore",
            _("line"): "s-g",
            _("end of [last] line"): "c-end",
            _("first non-blank char[acter] on line"): "g,g",
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
            _("((open|left) paren|previous sentence)"): "lparen",
            _("((close|right) paren|next sentence)"): "rparen",
            _("((left|open) curly brace|previous paragraph)"): "lbrace",
            _("((right|close) curly brace|next paragraph)"): "rbrace",
            _("next section start"): "rbracket,rbracket",
            _("next section end"): "rbracket,lbracket",
            _("previous section start"): "lbracket,rbracket",
            _("previous section end"): "lbracket,lbracket",
            ###########
            #  other  #
            ###########
            _("ex"): "colon",
            ###########
            #  marks  #
            ###########
            # TODO: tighten char to [a-vA-Z0-9]
            _("mark <char>"): "backtick,%(char)s",
            _("mark <char> first non-blank"): "apostrophe,%(char)s",
            _("mark <char> [and] keep jumps"): "g,backtick,%(char)s",
            _("mark <char> first non-blank [and] keep jumps"): "g,apostrophe,%(char)s",
            _("first char[acter] of last (change|yank)"): "apostrophe,lbracket",
            _("last char[acter] of last (change|yank)"): "apostrophe,rbracket",
            _("start of last selection"): "apostrophe,langle",
            _("end of last selection"): "apostrophe,rangle",
            _("restore position"): "apostrophe,apostrophe",
            _("restore position at last buffer exit"): "apostrophe,dquote",
            _("restore position at last insert"): "apostrophe,caret",
            _("restore position at last change"): "apostrophe,period",
            _("first non-blank char[acater] of next lowercase mark"): "rbracket,apostrophe",
            _("next lowercase mark"): "rbracket,backtick",
            _("first non-blank char[acter] of previous lowercase mark"): "lbracket,apostrophe",
            _("previous lowercase mark"): "lbracket,backtick",
            #####################
            #  various motions  #
            #####################
            _("(percent|match of next item)"): "percent",
            _("previous unmatched (open|left) paren"): "lbracket,lparen",
            _("previous unmatched (open|left) [curly] brace"): "lbracket,lbrace",
            _("next unmatched (close|right) paren"): "rbracket,rparen",
            _("next unmatched (close|right) [curly] brace"): "rbracket,rbrace",
            _("next start of method"): "rbracket,m",
            _("next end of method"): "rbracket,s-m",
            _("previous start of method"): "lbracket,m",
            _("previous end of method"): "lbracket,s-m",
            _("previous unmatched macro"): "lbracket,hash",
            _("next unmatched macro"): "rbracket,hash",
            _("previous start of comment"): "lbracket,asterisk",
            _("next end of comment"): "rbracket,asterisk",
            _("line from top"): "s-h",
            _("middle [of (window|screen)]"): "s-m",
            _("line from bottom"): "s-l",
            }
        self.extras = [
            RuleRef(name='char', rule=AnyCharacter())]

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

    def __init__(self, *args, **kwargs):
        self.spec = _(
            "<operator> "
            "(<line>|[to] "
            "(<motion>|<operatormotion>) "
            "[<numbers>] "
            "[<mode> mode])")
        self.extras = [
            Choice(name='operator', choices={
                _('change'): 'c',
                _('delete'): 'd',
                _('yank'): 'y',
                _('swap case'): 'g,tilde',
                _('make lowercase'): 'g,u',
                _('make uppercase'): 'g,s-u',
                _('filter'): 'exclamation',
                _('C filter'): 'equal',
                _('text formatting'): 'g,q',
                _('rotation 13 encoding'): 'g,question',
                _('shift right'): 'rangle',
                _('shift left'): 'langle',
                _('define fold'): 'z,f',
                _('call function'): 'g,at'}),
            Literal(name='line', text=_('line')),
            Repetition(
                name='numbers',
                child=RuleRef(rule=Number()),
                min=0,
                max=3),
            RuleRef(name='motion', rule=MotionRule()),
            RuleRef(name='operatormotion', rule=VisualMotionRule()),
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
        cmd_elements.append(
            node.get_child_by_name('operator').value())

        #########################
        #  operator repetition  #
        #########################
        # e.g: delete line : dd
        if node.has_child_with_name('line'):
            cmd_elements.append(cmd_elements[-1])

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
            _("interrupt"): "c-c",
            _("display file name"): "c-g",
            _("redraw screen"): "c-l",
            _("suspend"): "c-z",
            _("store and exit"): "s-z,s-z",
            _("unsafe exit"): "s-z,s-q",
            _("edit alternate"): "c-caret",
            _("help"): "f1",
            ###########
            #  jumps  #
            ###########
            _("next jumplist"): "c-i",
            _("previous jumplist"): "c-o",
            _("previous changelist"): "g,semicolon",
            _("next changlist"): "g,comma",
            ###########
            #  marks  #
            ###########
            _("set mark <char>"): "m,%(char)s",
            _("set previous mark"): "m,apostrophe",
            _("set (open|left) [square] bracket mark"): "m,lbracket",
            _("set (close|right) [square] bracket mark"): "m,rbracket",
            _("set (open|left) angle bracket mark"): "m,langle",
            _("set (close|right) angle bracket mark"): "m,rangle",
            ###############
            #  scrolling  #
            ###############
            _("scroll down half"): "c-d",
            _("scroll extra up"): "c-e",
            _("scroll forward screen"): "c-f",
            _("scroll back screen"): "c-b",
            _("scroll down"): "c-y",
            _("scroll half up"): "c-u",
            ###########
            #  modes  #
            ###########
            _("insert"): "i",
            _("insertmode"): "c-backslash,c-g",
            _("insert at start of line"): "s-i",
            _("insert on newline"): "o",
            _("insert on newline before"): "s-o",
            _("append"): "a",
            _("(cap|big) append"): "s-a",
            _("substitute"): "s",
            _("replace [mode]"): "s-r",
            _("external [mode]"): "s-q",
            _("visual"): "v",
            _("visual line"): "s-v",
            _("visual block"): "c-v",
            ######################
            #  undo/redo/repeat  #
            ######################
            _("redo"): "c-r",
            _("undo"): "u",
            _("undo on line"): "s-u",
            _("(repeat|period)"): "dot",
            _("(at|repeat register <register>)"): "at,%(register)s",
            _("repeat previous register repeat"): "at,at",
            _("repeat ex"): "at,colon",
            _("(ampersand|repeat [last] (search|replace))"): "ampersand",
            _("(semicolon|repeat (find|tag))"): "semicolon",
            _("(comma|reverse repeat (find|tag))"): "comma",
            _("record <register>"): "q,%(register)s",
            _("stop recording"): "q",
            _("edit ex"): "q,colon",
            _("edit search"): "q,slash",
            _("edit backward search"): "q,question",
            ##################
            #  text editing  #
            ##################
            _("addition"): "c-a",
            _("subtract"): "c-x",
            _("indent"): "c-rbracket",
            _("join lines"): "s-j",
            _("delete char[acter]"): "x",
            _("backwards delete char[acter]"): "s-x",
            _("replace <char>"): "r,%(char)s",
            _("(tilde|switch case)"): "tilde",
            ####################
            #  copy and paste  #
            ####################
            _("copy to end of line"): "s-c",
            _("paste"): "p",
            _("paste before"): "s-p",
            _("register <register>"): "dquote,%(register)s",
            _("diff get"): "do",
            _("diff put"): "dp",
            ############
            #  search  #
            ############
            _("lookup keyword"): "s-k",
            _("backward next"): "s-n",
            _("next"): "n",
            _("after <char>"): "t,%(char)s",
            _("backward move after <char>"): "s-t,%(char)s",
            _("tag older"): "c-t",
            _("(hash|backward search)"): "hash",
            _("(asterisk|forward search)"): "asterisk",
            _("(slash|search)"): "slash",
            _("(question [mark]|backward search)"): "question",
            ############
            #  window  #
            ############
            _("window increase height"): "c-w,plus",
            _("window decrease height"): "c-w,hyphen",
            _("window increase width"): "c-w,rangle",
            _("window decrease width"): "c-w,langle",
            _("window equalise"): "c-w,equal",
            _("window move (H|hotel|left)"): "c-w,s-h",
            _("window move (J|juliet|down)"): "c-w,s-j",
            _("window move (K|kilo|up)"): "c-w,s-k",
            _("window move (L|lima|right)"): "c-w,s-l",
            _("window preview"): "c-w,s-p",
            _("window rotate up"): "c-w,s-r",
            _("window move to [new] tab"): "c-w,s-t",
            _("window previous"): "c-w,s-w",
            _("window split and jump"): "c-w,rbracket",
            _("window split and edit alternate"): "c-w,caret",
            _("window set height"): "c-w,underscore",
            _("window bottom"): "c-w,b",
            _("window close"): "c-w,c",
            _("window split and jump to definition"): "c-w,d",
            _("window split and edit file"): "c-w,f",
            _("window split edit file and jump"): "c-w,s-f",
            # TODO: add c-w,g,] and c-w,g,}
            _("window tab and edit file"): "c-w,g,f",
            _("window tab edit file and jump"): "c-w,g,s-f",
            _("window (H|hotel|left)"): "c-w,h",
            _("window split and jump to declaration"): "c-w,i",
            _("window (J|juliet|down)"): "c-w,j",
            _("window (K|kilo|up)"): "c-w,k",
            _("window (L|lima|right)"): "c-w,l",
            _("window new"): "c-w,n",
            _("window only"): "c-w,o",
            _("window last"): "c-w,p",
            _("window rotate"): "c-w,r",
            _("window split [horizontal]"): "c-w,s",
            _("window top"): "c-w,t",
            _("window split vertical"): "c-w,v",
            _("window next"): "c-w,w",
            _("window exchange"): "c-w,x",
            _("window close preview"): "c-w,z",
            _("window width"): "c-w,bar",
            _("window tag in preview"): "c-w,rbrace",
            }
        self.extras = [
            # TODO: tighten register to [a-zA-Zs-9.%#:-"]
            RuleRef(name='register', rule=AnyCharacter()),
            RuleRef(name='char', rule=AnyCharacter())]

        MappingRule.__init__(self, *args, **kwargs)

####################################
#  Rules for true vim normal mode  #
####################################

class TrueVimNormalRule(CompoundRule):

    """All the repeatable commands for vim's normal mode."""

    exported = False

    def __init__(self, *args, **kwargs):
        self.spec = _("<cmd>")
        self.extras = [
            Alternative(name='cmd', children=(
                RuleRef(
                    name='motion_operator',
                    rule=MotionOperatorRule()),
                RuleRef(
                    name='motion', rule=MotionRule()),
                RuleRef(
                    name='normal', rule=VimNormalRule()),
                RuleRef(name='number', rule=Number()),
                ))
            ]

        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        if node.has_child_with_name('motion_operator'):
            return node.get_child_by_name(
                'motion_operator').value()
        elif node.has_child_with_name('motion'):
            return node.get_child_by_name(
                'motion').value()
        elif node.has_child_with_name('normal'):
            return node.get_child_by_name(
                'normal').value()
        elif node.has_child_with_name('number'):
            return node.get_child_by_name(
                'number').value()
        else:
            pass

    def _process_recognition(self, node, extras):
        Key(self.value(node)).execute()

class TrueVimNormalRepetitionRule(CompoundRule):

    """Repeat TrueVimNormalRule."""

    def __init__(self, *args, **kwargs):
        self.spec = _("<cmds>")
        self.extras = [
            Repetition(
                name='cmds',
                child=RuleRef(rule=TrueVimNormalRule()),
                min=1,
                max=5)
            ]

        CompoundRule.__init__(self, *args, **kwargs)

    def value(self, node):
        extras = extract_values(node, (
            TrueVimNormalRule), recurse=True)
        return ','.join(extras)

    def _process_recognition(self, node, extras):
        Key(self.value(node)).execute()


TRUE_VIM_NORMAL_GRAMMAR = None

def load():
    """Register grammar."""
    global TRUE_VIM_NORMAL_GRAMMAR
    TRUE_VIM_NORMAL_GRAMMAR = Grammar(
        'true_vim_normal_mode',
        context=vim_normal_mode())
    TRUE_VIM_NORMAL_GRAMMAR.add_rule(
        TrueVimNormalRepetitionRule())
    TRUE_VIM_NORMAL_GRAMMAR.load()

    print 'vim grammars: Loaded.'
    # print TRUE_VIM_NORMAL_GRAMMAR.get_complexity_string()

def unload():
    """Unregister grammar."""
    global TRUE_VIM_NORMAL_GRAMMAR
    if TRUE_VIM_NORMAL_GRAMMAR is None:
        TRUE_VIM_NORMAL_GRAMMAR.unload()
        TRUE_VIM_NORMAL_GRAMMAR = None
