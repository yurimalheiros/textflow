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
This module implements the trigger of "ctrl+shift+l".
"""

import tf.app

shortcut = "ctrl+shift+l"
sticky = False

class SelectLine(object):
    
    def activate(self):
        """
        Trigger activator.
        """
        
        self.document_manager = tf.app.document_manager
        buffer = self.document_manager.get_active_view().buffer
        
        insert_mark = buffer.get_insert()
        start = buffer.get_iter_at_mark(insert_mark)
        end = start.copy()
#        self.__get_word_bounds(start, end)
        if not end.ends_line():
            end.forward_to_line_end()
        line_num = start.get_line()
        start = buffer.get_iter_at_line(line_num)
        buffer.select_range(end, start)
        
        return True
        
#    def __get_word_bounds(self, begin, end):
#        
#        # Find begin bound
#        char = begin.get_char()
#        while True:
#            if begin.starts_line():
#                break
#            else:
#                begin.backward_char()
#            char = begin.get_char()
#                
#        # Find end bound
#        while True:
#            char = end.get_char()
#            if end.ends_line():
#                break
#            else:
#                end.forward_char()
#                    
#        return (begin, end)

