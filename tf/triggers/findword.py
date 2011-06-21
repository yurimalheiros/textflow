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
This module implements the trigger of "ctrl+8".
"""

import tf.app

shortcut = "ctrl+8"
sticky = False

class FindWord(object):
    
    def activate(self):
        """
        Operations before trigger activation.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        
        insert_mark = buffer.get_insert()
        begin = buffer.get_iter_at_mark(insert_mark)
        end = begin.copy()
        self.__get_word_bounds(begin, end)
        
        word = buffer.get_text(begin, end)
        
        search_bar = tf.app.main_window.search_bar
        search_bar.show_bar()
        search_bar.entry.set_text(word)
        view.grab_focus()
        
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
