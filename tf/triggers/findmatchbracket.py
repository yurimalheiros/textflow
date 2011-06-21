# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Yuri Malheiros.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#######################################################################

"""
This module implements the trigger of "ctrl+[".
"""

import tf.app

shortcut = "ctrl+["
sticky = False

class FindMatchBracket(object):
    
    def activate(self):
        """
        Operations on trigger activation.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        open_brackets = {'(' : ')', '[' : ']', '{' : '}'}
        close_brackets = {')' : '(', ']' : '[', '}' : '{'}
        
        insert_mark = buffer.get_insert()
        begin = buffer.get_iter_at_mark(insert_mark)
        end = begin.copy()
        end.backward_char()
        
        begin_char = begin.get_char()
        end_char = end.get_char()
        
        if begin_char in open_brackets.keys():
            new_pos = self.__search_close_match(begin, begin_char,
                                                open_brackets[begin_char])
        elif begin_char in close_brackets.keys():
            new_pos = self.__search_open_match(begin, begin_char,
                                               close_brackets[begin_char])
        elif end_char in open_brackets.keys():
            new_pos = self.__search_close_match(end, end_char,
                                                open_brackets[end_char])
        elif end_char in close_brackets.keys():
            new_pos = self.__search_open_match(end, end_char,
                                               close_brackets[end_char])
        else:
            return True
        
        buffer.place_cursor(new_pos)
        
        return True
        
    def __search_close_match(self, iterator, char, match):
        iter = iterator.copy()
        cont = 1
        
        while iter.forward_char():
            c = iter.get_char()
            if c == char:
                cont+=1
            elif c == match:
                cont-=1
            
            if cont == 0:
                return iter
        
        return iterator
        
    def __search_open_match(self, iterator, char, match):
        iter = iterator.copy()
        cont = 1
        
        while iter.backward_char():
            c = iter.get_char()
            if c == char:
                cont+=1
            elif c == match:
                cont-=1
            
            if cont == 0:
                return iter
        
        return iterator

