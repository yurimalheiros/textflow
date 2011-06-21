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
This module implements the trigger of "}".
"""

import tf.app

shortcut = "}"
sticky = False

class CurlyClose(object):
    
    def activate(self):
        """
        Operations before trigger activation.
        """
        self.document_manager = tf.app.document_manager
        buffer = self.document_manager.get_active_view().buffer
        
        insert_mark = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert_mark)
        
        next_char = insert_iter.get_char()
        if next_char == "}":
            insert_next_iter = insert_iter.copy()
            insert_next_iter.forward_chars(1)
            buffer.place_cursor(insert_next_iter)
            return True
        else:
            return False

