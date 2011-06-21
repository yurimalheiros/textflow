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
This module implements the trigger of "shift+tab".
"""

import tf.app

shortcut = "shift+" + u'\ufe20'
sticky = False

class ShiftTab(object):
    
    def activate(self):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        document = self.document_manager.get_active_document()
        buffer = document.view.buffer
        snippets = document.snippets
        
        if len(snippets.stack) > 0:
            insert = buffer.get_insert()
            
            if snippets.valid_cursor_position():
                for i in range(len(snippets.stack)):
                    try:
                        snippets.previous_field()
                    except KeyError:
                        ins_iter = buffer.get_iter_at_mark(insert)
                        buffer.select_range(ins_iter, ins_iter)
                        snippets.pop_snippet()
                    else:
                        break
                    
            else:
                snippets.pop_snippet()
            return True
            
        else:        
            return False

