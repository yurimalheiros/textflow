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
This module implements the trigger of "{".
"""

import tf.app

shortcut = "{"
sticky = False

class CurlyOpen(object):
    
    def activate(self):
        """
        If self.surround is False - Auto complete parenthesis
        If self.surround is True - Surround selection.
        """
        
        self.document_manager = tf.app.document_manager
        buffer = self.document_manager.get_active_view().buffer
        
        if buffer.get_has_selection():
            start, end = buffer.get_selection_bounds()
            text = buffer.get_text(start, end)
            buffer.delete(start, end)
            buffer.insert_at_cursor("{" + text + "}")
        else:
            # Auto complete operation
            insert_mark = buffer.get_insert()
            buffer.insert_at_cursor("{}")
            insert_iter = buffer.get_iter_at_mark(insert_mark)
            insert_iter.backward_chars(1)
            buffer.place_cursor(insert_iter)

        return True

