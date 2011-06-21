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
This module implements the trigger of "ctrl+d".
"""

import gtk
import tf.app

shortcut = "ctrl+d"
sticky = True
sticky_keys = (u'\uff51', u'\uff52', u'\uff53', u'\uff54', u'\uff55',
               u'\uff56')

class DeleteLine(object):
    
    """
    This class implements the delete line operation.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        self.start_line = None
        self.end_line = None
        self.id = None
        self.buffer = None
        
#         self.document_manager.connect("switch-page", self.tab_switch)
    
    def activate(self):
        """
        Delete current line.
        """
        self.document_manager = tf.app.document_manager
        view = self.document_manager.get_active_view()
        self.buffer = view.buffer
        if self.id != None:
            self.buffer.disconnect(self.id)
            self.id = None
        self.id = self.buffer.connect("mark-set", self.cursor_moved, 
                                      self.buffer)
            
        self.buffer.begin_user_action()
        view.do_move_cursor(view, gtk.MOVEMENT_PARAGRAPH_ENDS, -1, 0)
        itstart = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        
#        view.backward_display_line_start(itstart)
        
        self.start_line = itstart.get_line()
        
        itstart = self.buffer.get_iter_at_line(self.start_line)
        
        itend = self.buffer.get_iter_at_mark(self.buffer.get_insert())
#        view.forward_display_line_end(itend)
        
        if not itend.ends_line():
            itend.forward_to_line_end()
#        line = self.buffer.get_slice(itstart, itend, True)
        
        self.buffer.apply_tag_by_name("sticky", itstart, itend)
#         buffer.delete(itstart, itend);
        self.buffer.end_user_action()
    
    def sticky_release(self):
        
        if self.start_line > self.end_line:
            aux = self.start_line
            self.start_line = self.end_line
            self.end_line = aux
        
        start_iter = self.buffer.get_iter_at_line(self.start_line)
        end_iter = self.buffer.get_iter_at_line(self.end_line)
        
#        end_iter.forward_line()
        
#        view.forward_display_line_end(end_iter)
        end_iter.forward_line()

        self.buffer.delete(start_iter, end_iter)
        siter = self.buffer.get_start_iter()
        eiter = self.buffer.get_end_iter()
        self.buffer.remove_tag_by_name("sticky", siter, eiter)

        if self.id != None:
            self.buffer.disconnect(self.id)
            self.id = None
    
    def cursor_moved(self, widget, iter, textmark, buffer):
        insert_mark = buffer.get_insert()
        if textmark == insert_mark:
            temp = self.end_line
            self.end_line = buffer.get_iter_at_mark(insert_mark).get_line()
            if self.end_line > self.start_line:
#                 print "end line > start line"
                if self.end_line >= temp:
                    self.__color_line(self.end_line)
                else:
                    self.__uncolor_line(temp)
            elif self.end_line < self.start_line:
#                 print "end line < start line"
                if self.end_line < temp:
                    self.__color_line(self.end_line)
                else:
                    self.__uncolor_line(temp)
            else:
                if temp != self.end_line:
                    self.__uncolor_line(temp)
    
    def __color_line(self, num):
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        start_iter = buffer.get_iter_at_line(num)
        end_iter = start_iter.copy()
#        view.forward_display_line_end(end_iter)
        
        if not end_iter.ends_line():
            end_iter.forward_to_line_end()

        buffer.apply_tag_by_name("sticky", start_iter, end_iter)
    
    def __uncolor_line(self, num):
        view = self.document_manager.get_active_view()
        buffer = view.buffer
        start_iter = buffer.get_iter_at_line(num)
        end_iter = start_iter.copy()
        end_iter.forward_line()
        buffer.remove_tag_by_name("sticky", start_iter, end_iter)
#         
#     def tab_switch(self, widget, page, page_num):
#         view = self.document_manager.get_active_view()
#         buffer = view.buffer
#         
#         print "desconnect"
#         if self.id != None:
#             buffer.disconnect(self.id)
#             
#             start = buffer.get_start_iter()
#             start = buffer.get_start_iter()
#             
#             self.id = None
