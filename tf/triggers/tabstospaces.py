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
This module implements the trigger of "ctrl+2".

Thanks to Tab Convert Gedit Plugin by Frederic Back.
"""

import tf.app

shortcut = "ctrl+2"
sticky = False

class TabsToSpaces(object):

    def activate(self):
        """
        Operations before trigger activation.
        """
        self.document_manager = tf.app.document_manager
        document = self.document_manager.get_active_document()
        buffer = document.view.buffer
        
        tab_size = document.view.get_tab_width()
        text = document.get_text()
        text = text.expandtabs(tab_size)
        
        buffer.begin_user_action()
        
        start_iter = buffer.get_start_iter() 
        end_iter = buffer.get_end_iter()
        
        buffer.delete(start_iter, end_iter)
        buffer.insert(start_iter, text)
        
        buffer.end_user_action()
        
        return True
