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
This module implements the trigger of "ctrl+shift+u".
"""

import tf.app

shortcut = "ctrl+shift+u"
sticky = False

class LowerCase(object):
    
    def activate(self):
        """
        Snippet active.
        """
        self.document_manager = tf.app.document_manager
        buffer = self.document_manager.get_active_view().buffer
        
        if buffer.get_has_selection():
            start, end = buffer.get_selection_bounds()
            text = unicode(buffer.get_text(start, end))
            buffer.begin_user_action()
            buffer.delete(start, end)
            buffer.insert_at_cursor(text.lower())
            buffer.end_user_action()
        else:
            insert_mark = buffer.get_insert()
            start = buffer.get_iter_at_mark(insert_mark)
            index = start.get_line_offset()
            end = start.copy()
            self.__get_word_bounds(start, end)
            text = unicode(buffer.get_text(start, end))
            buffer.begin_user_action()
            
            buffer.delete(start, end)
            buffer.insert_at_cursor(text.lower())
            new_insert_iter = buffer.get_iter_at_mark(insert_mark)
            new_insert_iter.set_line_offset(index)
            buffer.place_cursor(new_insert_iter)
            
            buffer.end_user_action()

        return True
        
    def __get_word_bounds(self, begin, end):
        if begin.starts_word():
            end.forward_word_end()
        elif end.ends_word():
            begin.backward_word_start()
        elif begin.inside_word():
            begin.backward_word_start()
            end.forward_word_end()
                       
        return (begin, end)
