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
This module implements a class that represents a snippet field.
"""

import gobject
import gtk

class SnippetField(gobject.GObject):

    __gsignals__ = { "changed" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                 (gobject.TYPE_STRING,)) }


    def __init__(self, view, num, marks):
        """
        Constructor.
        
        @param buffer: The SourceBuffer where the snippet will be inserted.
        @type buffer: A SourceBuffer object.
        
        @param marks: The marks at the bounds of snippet field.
        @type marks: A tuple.
        """
        gobject.GObject.__init__(self)
        self.view = view
        self.buffer = view.buffer
        self.num = num
        self.marks = marks
        self.id = None
        
        self.id = self.view.connect('event-after', self.insert_text)
    
    #################### Signals ####################
        
    def insert_text(self, widget, event):
        """
        When something is typed inside this snippet field a signal is emited.
        """
        
        if event.type != gtk.gdk.KEY_PRESS:
            return False

        invalid_keys = (65509, 65505, 65507, 65513, 65527, 65508, 65360, 65367,
                        65365, 65366, 65379, 65361, 65362, 65363, 65364, 65289,
                        65056)
        
        # Skip tab, shift+tab and other special keys.
        if event.keyval in invalid_keys:
            return False
            
        start = self.buffer.get_iter_at_mark(self.marks[0])
        end = self.buffer.get_iter_at_mark(self.marks[1])
        all_text = self.buffer.get_text(start, end)
        insert_mark = self.buffer.get_insert()
        iter = self.buffer.get_iter_at_mark(insert_mark)

        if iter.in_range(start, end) or start.equal(iter) or end.equal(iter):
            self.emit("changed", all_text)
