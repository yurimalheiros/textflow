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

class SnippetMirror(gobject.GObject):


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
        self.regexp = None

