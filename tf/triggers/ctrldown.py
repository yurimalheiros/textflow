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
This module implements the trigger of "ctrl+down arrow".
"""

import gtk
import tf.app

shortcut = "ctrl+" + u'\uff54'
sticky = False

class CtrlDown(object):
    
    def __init__(self):
        """
        Constructor.
        """
        self.current_iters = [None, None]
        self.up_iters = [None, None]
        self.view = None
        self.buffer = None
        self.current_line = None
        self.up_line = None
        self.goto_line = 0
        
    def activate(self):
        """
        Operations after trigger activation.
        """
        self.document_manager = tf.app.document_manager
        self.document = self.document_manager.get_active_document()
        self.view = self.document.view
        self.buffer = self.view.buffer
        
        select_flag = False
        
        if self.buffer.get_has_selection():
            # Getting iters at begin of the selection first line
            # and at end of the selection last line
            selection_iters = self.buffer.get_selection_bounds()
            
            if not selection_iters[1].ends_line():
                selection_iters[1].forward_to_line_end()
            
            line_num = selection_iters[0].get_line()
            self.current_iters = self.buffer.get_iter_at_line(line_num), selection_iters[1]
            
            # Getting iters at begin and end of the line above selection
            self.up_iters[0] = self.current_iters[1].copy()
            self.up_iters[1] = self.current_iters[1].copy()
            self.up_iters[0].forward_line()
            self.up_iters[1].forward_line()
            
            if not self.up_iters[1].ends_line():
                self.up_iters[1].forward_to_line_end()
                
            select_flag = True
                    
        else:
            self.current_iters = self.document.get_line_iters()
            
            # Getting iters at begin and end of the line above selection
            self.view.do_move_cursor(self.view, gtk.MOVEMENT_PARAGRAPH_ENDS, -1, 0)
            
            self.up_iters[0] = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            self.up_iters[1] = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            self.up_iters[0].forward_line()
            self.up_iters[1].forward_line()
            
            if not self.up_iters[1].ends_line():
                self.up_iters[1].forward_to_line_end()
        
            
        self.goto_line = self.up_iters[0].get_line() + 1
            
        if not self.current_iters[1].is_end():
            
            self.current_line = self.buffer.get_text(self.current_iters[0], self.current_iters[1], True)
            self.up_line = self.buffer.get_text(self.up_iters[0], self.up_iters[1],True) 
            
            self.buffer.begin_user_action()

            self.buffer.delete(self.current_iters[0], self.up_iters[1])
            
            if select_flag:
                insert_mark = self.buffer.get_insert()
                insert_iter = self.buffer.get_iter_at_mark(insert_mark)
                mark_aux = self.buffer.create_mark("aux", insert_iter, False)
                mark_right = self.buffer.create_mark("right", insert_iter, False)
            

            self.buffer.insert_at_cursor(self.up_line + "\n")
                        
            if select_flag:
                aux_iter = self.buffer.get_iter_at_mark(mark_aux)
                mark_left = self.buffer.create_mark("left", aux_iter, True)
            
            
                mark_left.set_visible(True)               
                mark_right.set_visible(True)               
            
            self.buffer.insert_at_cursor(self.current_line)
            
            self.document_manager.search_functions.goto_line(self.goto_line, False)
            self.current_mark = self.buffer.get_insert()
            self.view.scroll_mark_onscreen(self.current_mark)

            if select_flag:
                iter_left = self.buffer.get_iter_at_mark(mark_left)
                iter_right = self.buffer.get_iter_at_mark(mark_right)
                self.buffer.select_range(iter_right, iter_left)
                
                self.buffer.delete_mark(mark_left)
                self.buffer.delete_mark(mark_right)
                self.buffer.delete_mark(mark_aux)
            
            self.buffer.end_user_action()
            
        return True
