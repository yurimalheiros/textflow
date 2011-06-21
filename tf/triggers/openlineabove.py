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
This module implements the trigger of "ctrl+shift+return".
"""

import tf.app

shortcut = 'ctrl+shift+' + unichr(65293) #Ctrl+Shift+Return
sticky = False

class OpenLineAbove(object):
    
    def activate(self):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        self.document = self.document_manager.get_active_document()
        self.view = self.document.view
        self.buffer = self.view.buffer
        
        cursor_iter = self.__get_cursor_iter()
        
        if not cursor_iter.starts_line():
            cursor_iter.set_line(cursor_iter.get_line())
        
        self.buffer.begin_user_action()
        
        self.buffer.place_cursor(cursor_iter)
        self.buffer.insert_at_cursor("%s\n" % self.document.get_indentation(cursor_iter))
        
        cursor_iter = self.__get_cursor_iter()
        
        cursor_iter.backward_line()
        
        if not cursor_iter.ends_line():
            cursor_iter.forward_to_line_end()
        
        self.buffer.place_cursor(cursor_iter)
        
        self.buffer.end_user_action()
        
        return True
        
    def __get_cursor_iter(self):
        return self.buffer.get_iter_at_mark(self.buffer.get_insert())
        