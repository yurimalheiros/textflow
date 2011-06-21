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
This module implements the trigger of "shift+end".
"""

import tf.app

shortcut = "shift+" +  u'\uff57'
sticky = False

class SmartEndSelection(object):
    
    """
    This class implements the smart end selection operation.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.start_iter = None
        self.end_iter = None
    
    def activate(self):
        """
        Operations before trigger activation.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        has_selection = buffer.get_has_selection()
        
        insert_mark = buffer.get_insert()
        
        self.start_iter = buffer.get_iter_at_mark(insert_mark)

        if has_selection:
            sel_mark = buffer.get_selection_bound()
            self.start_iter = buffer.get_iter_at_mark(sel_mark)
            self.end_iter = buffer.get_iter_at_mark(insert_mark)
            
            if self.end_iter.ends_line():
                self.__find_smart_start(self.end_iter)
            else:
                self.end_iter.forward_char()
                while True:
                    char = self.end_iter.get_char()
                    if self.end_iter.ends_line():
                        view.forward_display_line_end(self.end_iter)
                        break
                    
                    if char != " " and char != "\t":
                        view.forward_display_line_end(self.end_iter)
                        self.__find_smart_start(self.end_iter)
                        break
                    else:
                        self.end_iter.forward_char()
        else:
            self.end_iter = self.start_iter.copy()
            while True:
                char = self.end_iter.get_char()
                if self.end_iter.ends_line():
                    view.forward_display_line_end(self.end_iter)
                    break
                
                if char != " " and char != "\t":
                    view.forward_display_line_end(self.end_iter)
                    self.__find_smart_start(self.end_iter)
                    break
                else:
                    self.end_iter.forward_char()
        
        buffer.select_range(self.end_iter, self.start_iter)
        view.scroll_to_mark(buffer.get_insert(), 0)
        return True

    def __find_smart_start(self, iterator):
        """
        This method puts a iter at the smart end of it line.
        
        @param iterator: A text iter that will be
        put at the smart end of it line.
        @type iterator: A TextIter object.
        """
        while True:
            char = iterator.get_char()
            if char == " " or char == "\t" or char == unichr(0) \
            or char == "\n" or char == "\r":
                if iterator.starts_line():
                    return
                else:
                    iterator.backward_char()
            else:
                iterator.forward_char()
                return
        return
    
