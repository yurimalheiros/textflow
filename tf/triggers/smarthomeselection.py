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
This module implements the trigger of "shift+home".
"""

import tf.app

shortcut = "shift+" + u'\uff50'
sticky = False

class SmartHomeSelection(object):
    
    """
    This class implements the delete line operation.
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
            
            if self.end_iter.starts_line():
               self.__find_smart_start(self.end_iter)
            else:
                self.end_iter.backward_char()
                while True:
                    char = self.end_iter.get_char()
                    if self.end_iter.starts_line():
                        view.backward_display_line_start(self.end_iter)
                        break
                    
                    if char != " " and char != "\t":
                        view.backward_display_line_start(self.end_iter)
                        self.__find_smart_start(self.end_iter)
                        break
                    else:
                        self.end_iter.backward_char()
        else:
            self.end_iter = self.start_iter.copy()
           
            if self.end_iter.starts_line():
                self.__find_smart_start(self.end_iter)
            else:
                self.end_iter.backward_char()
                while True:
                    char = self.end_iter.get_char()
                    if self.end_iter.starts_line():
                        view.backward_display_line_start(self.end_iter)
                        break
                    
                    if char != " " and char != "\t":
                        view.backward_display_line_start(self.end_iter)
                        self.__find_smart_start(self.end_iter)
                        break
                    else:
                        self.end_iter.backward_char()
    
        buffer.select_range(self.end_iter, self.start_iter)
        view.scroll_to_mark(buffer.get_insert(), 0)
        return True

    def __find_smart_start(self, iterator):
        """
        This method puts a iter at the smart start of it line.
        
        @param iterator: A text iter that will be
        put at the smart start of it line.
        @type iterator: A TextIter object.
        """
        while True:
            char = iterator.get_char()
            if char == " " or char == "\t":
                iterator.forward_char()
            else:
                return
        return
    
