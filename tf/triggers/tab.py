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
This module implements the trigger of "tab".
"""

import tf.app

shortcut = u'\uff09'
sticky = False

class Tab(object):
    
    """
    This class implements all functions of tab shortcut.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.snippet_flag = False
         
    def activate(self, snippet=None):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        snippets = self.document_manager.get_active_document().snippets
        
        self.snippet_flag = snippets.active()
        
        if not self.snippet_flag:
            if len(snippets.stack) > 0:
                if snippets.valid_cursor_position():
                    for i in range(len(snippets.stack)):
                        try:
                            snippets.next_field()
                        except KeyError:
                            end_mark = snippets.stack[-1].stop
                            
                            if end_mark != None:
                                buffer.place_cursor(buffer.get_iter_at_mark(end_mark))
                            else:
                                end_bound_mark = snippets.stack[-1].bounds[1]
                                buffer.place_cursor(buffer.get_iter_at_mark(end_bound_mark))
#                                buffer.insert_at_cursor("\t")
                                
                            snippets.pop_snippet()
                        else:
                            break
                else:
                    snippets.pop_snippet()
#                    buffer.insert_at_cursor("\t")
                    return False
                return True
            else:
                return False
        else:
            return True
#        self.snippet_flag = False
#        
#        return True
