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
This module implements the trigger of "ctrl+return".
"""

import tf.app

shortcut = 'ctrl+' + unichr(65293) #Ctrl+Return
sticky = False

class OpenLine(object):
    
    def activate(self):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        self.document = self.document_manager.get_active_document()
        self.view = self.document.view
        self.buffer = self.view.buffer
        
        cursor_iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        
        if not cursor_iter.ends_line():
            cursor_iter.forward_to_line_end()
        
        self.buffer.begin_user_action()
        
        self.buffer.place_cursor(cursor_iter)
        self.buffer.insert_at_cursor("\n%s" % self.document.get_indentation(cursor_iter))
        
        self.buffer.end_user_action()
        
        return True
        