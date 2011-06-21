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
This module implements the trigger of "ctrl+j".
"""

import tf.app

shortcut = "ctrl+j"
sticky = False

class DuplicateLine(object):
    
    def activate(self):
        """
        Duplicate current line.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        
        insert_mark = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert_mark)
        cursor_offset = insert_iter.get_line_offset()
        start = insert_iter
        end = start.copy()
        
        if buffer.get_has_selection():
            start, end = buffer.get_selection_bounds()
            
            insert_iter = buffer.get_iter_at_mark(buffer.get_insert())
            if insert_iter.compare(end) == -1:
                delta_line_number = start.get_line() - end.get_line()
            else:
                delta_line_number = end.get_line() - start.get_line()
                
            self.__backward_to_line_start(start)
            self.__forward_to_line_end(end)
        else:
            self.__backward_to_line_start(start)
            self.__forward_to_line_end(end)
            delta_line_number = 0
        
        
        end_offset = end.get_offset()
        text = "\n" + buffer.get_text(start, end)
        buffer.begin_user_action()
        buffer.insert(end, text)
        buffer.end_user_action()
        iterator = buffer.get_iter_at_offset(end_offset)
        
        if delta_line_number >= 0:
            for i in range(delta_line_number + 1):
                iterator.forward_line()
        else:
            for i in range(delta_line_number, 0):
                iterator.forward_line()
        
        iterator.set_line_offset(cursor_offset)
        buffer.place_cursor(iterator)
        
        return True
    
    #TODO: Remover metodos que usam loop e usar metodos da API
    
    def __backward_to_line_start(self, iterator):
        """
        Put a iter at the start of it line.
        
        @param iterator: A text iter that will be put at the start of it line.
        @type iterator: A TextIter object.
        """
        while True:
            if iterator.starts_line():
                return
            iterator.backward_char()
        return
    
    def __forward_to_line_end(self, iterator):
        """
        Put a iter at the end of it line.
        
        @param iterator: A text iter that will be put at the end of it line.
        @type iterator: A TextIter object.
        """
        while True:
            if iterator.ends_line():
                return
            iterator.forward_char()
