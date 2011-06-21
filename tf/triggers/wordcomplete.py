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
This module implements the trigger of "ctrl+space".
"""

import re
import tf.app

shortcut = 'ctrl+ '
sticky = False

class WordComplete(object):
    
    def activate(self):
        """
        Activate word complete.
        """

        self.document_manager = tf.app.document_manager
        document = self.document_manager.get_active_document()
        view = self.document_manager.get_active_view()
        buffer = self.document_manager.get_active_view().buffer
        
        insert_mark = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert_mark)
        start_iter = insert_iter.copy()

        self.__find_word_start(start_iter)
        key = buffer.get_text(start_iter, insert_iter)
        
        if key != "":
            if document.word_complete.pw == None:
                document.word_complete.complete(key)
            return True
        else:
            return False
            
    
    def __find_word_start(self, iterator):
        """
        Move iterator to word start ignoring underlines.
        
        @param iterator: the iterator moved.
        @type iterator: a TextIter.
        """
        chars_regex = re.compile("[a-zA-Z_]")
        
        while iterator.backward_char():
            char = iterator.get_char()
    
            if chars_regex.match(char):
                continue
            else:
                iterator.forward_char()
                return True

        return True
        
       

