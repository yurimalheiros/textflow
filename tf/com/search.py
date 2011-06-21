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
This module implements a class responsible for search functions.
"""

import gtk
import re

class Search(object):
    """
    This class implements search operations.
    """
    def __init__(self, document_manager):
        self.document_manager = document_manager
        self.entry = None
        self.entry_replace = None
        self.matches = None
        self.matches_num = 0
        self.index = 0
        self.regexp = False
        self.view = None
        self.all_search = False
        
        self.color_red = gtk.gdk.Color(65535, 20000, 20000)
        self.color_white = gtk.gdk.Color(65535, 65535, 65535)
        self.color_black = gtk.gdk.Color(0, 0, 0)
        
    #################### Public Methods ####################
    
    def update_matches(self, begin, end):
        """
        This method updates the search matches between 2 iters
        
        @param begin: the start point of text where the matches will be updated
        @type begin: A TextIter object
        
        @param end: the end point of text where the matches will be updated
        @type end: A TextIter object
        """
        if self.entry != None:
            self.__get_matches(self.entry.get_text(), begin, end)
    
    def incremental(self):
        """
        This method call the operations to do de incremental search according
        with interface data.
        """
        self.__get_environment()
        self.all_search = True
        begin = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        self.__get_matches(self.entry.get_text(), begin, end)
        
        if self.matches != None:
            self.index = self.index_cursor
            start_iter = \
            self.buffer.get_iter_at_mark(self.matches[self.index][0])
            end_iter = \
            self.buffer.get_iter_at_mark(self.matches[self.index][1])
            
            self.buffer.select_range(start_iter, end_iter)
            self.view.scroll_to_iter(start_iter, 0, True)
        else:
            cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
            self.buffer.place_cursor(cursor_iter)
    
    def next(self):
        """
        Find the next match and select it.
        """
        if self.buffer.get_has_selection():
            self.__get_environment()
            begin = self.buffer.get_start_iter()
            end = self.buffer.get_end_iter()
            self.__get_matches(self.entry.get_text(), begin, end)
            
            if self.matches != None:
                if self.index < (self.matches_num - 1):
                    self.index += 1
                else:
                     self.index = 0
                     
                start_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][0])
                end_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][1])
                
                self.buffer.select_range(start_iter, end_iter)
                self.view.scroll_to_iter(start_iter, 0, True)
            else:
                cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
                self.buffer.place_cursor(cursor_iter)
        else:
            self.incremental()
    
    def previous(self):
        """
        Find the previous match and select it.
        """
        if self.buffer.get_has_selection():
            self.__get_environment()
            begin = self.buffer.get_start_iter()
            end = self.buffer.get_end_iter()
            self.__get_matches(self.entry.get_text(), begin, end)
            
            if self.matches != None:
                if self.index == 0:
                    self.index = self.matches_num - 1
                else:
                    self.index -= 1
                     
                start_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][0])
                end_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][1])
                
                self.buffer.select_range(start_iter, end_iter)
                self.view.scroll_to_iter(start_iter, 0, True)
            else:
                cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
                self.buffer.place_cursor(cursor_iter)
        else:
            self.incremental()
    
    def replace(self):
        """
        Replace the next match.
        """
        if not self.buffer.get_has_selection():
            self.next()
        else:
            if self.matches != None:
                self.buffer.begin_user_action()
                
                start_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][0])
                end_iter = \
                self.buffer.get_iter_at_mark(self.matches[self.index][1])
                
                self.buffer.delete(start_iter, end_iter)
                
                self.buffer.insert(start_iter, self.entry_replace.get_text())
                self.matches_num -= 1
                
                self.__get_environment()
                #begin = self.buffer.get_start_iter()
                #end = self.buffer.get_end_iter()
                
                #begin, end = self.view.get_line_iters()
                #self.__get_matches(self.entry.get_text(), begin, end)
                self.next()
                #if self.matches != None:
                if self.matches_num != 0:
                    if self.index > (self.matches_num - 1):
                        self.index = 0
                    
                    try:
                        start_iter = \
                        self.buffer.get_iter_at_mark(self.matches[self.index][0])
                        end_iter = \
                        self.buffer.get_iter_at_mark(self.matches[self.index][1])
                        
                        self.buffer.select_range(start_iter, end_iter)
                    except IndexError:
                        cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
                        self.buffer.place_cursor(cursor_iter)
                    else:
                        self.view.scroll_to_iter(start_iter, 0, True)
                self.buffer.end_user_action()
            else:
                cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
                self.buffer.place_cursor(cursor_iter)
        
    def replace_all(self):
        """
        Replace all matches.
        """
        
        self.__get_environment()
        begin = self.buffer.get_start_iter()
        end = self.buffer.get_end_iter()
        self.__get_matches(self.entry.get_text(), begin, end)
        
        if self.matches != None:
            num_replaces = self.matches_num
            matches = self.matches
            self.buffer.begin_user_action()
            
            for i in range(num_replaces):

                start_iter = \
                self.buffer.get_iter_at_mark(matches[i][0])
                end_iter = \
                self.buffer.get_iter_at_mark(matches[i][1])
                
                self.buffer.delete(start_iter, end_iter)
                
                self.buffer.insert(start_iter, self.entry_replace.get_text())
                
                self.__get_environment()
                begin = self.buffer.get_start_iter()
                end = self.buffer.get_end_iter()
                
            self.buffer.end_user_action()
        else:
            cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
            self.buffer.place_cursor(cursor_iter)
            
    def view_focus(self):
        """
        This method puts the cursor back to the TextView.
        """
        try:
            cursor_iter = \
            self.buffer.get_iter_at_mark(self.matches[self.index][0])
            self.buffer.place_cursor(cursor_iter)
        except (TypeError, IndexError):
            cursor = self.buffer.get_insert()
            cursor_iter = self.buffer.get_iter_at_mark(cursor)
            self.buffer.place_cursor(cursor_iter)
            
        self.view.grab_focus()

    def goto_line(self, line_num, scroll = True):
        """
        Change current line postion of cursor to line_num line.
        """
        iter = self.buffer.get_iter_at_line(line_num-1)
        self.buffer.place_cursor(iter)
        if scroll:
            self.view.scroll_to_iter(iter, 0, True)

    def check_last_line(self, gotoline):
        """
        This function check with line exists in active view, and change colors of entry if not.

        """
        try:       
            
             
            if gotoline == "":
                gotoline = 0 
            else:
                gotoline = int(gotoline) 

            if gotoline > self.buffer.get_end_iter().get_line() or gotoline < 0:
                if self.entry != None:
                    self.entry.modify_base(gtk.STATE_NORMAL,
                                                   self.color_red)
                    self.entry.modify_text(gtk.STATE_NORMAL,
                                                   self.color_white)
            else:
                if self.entry != None:
                    self.entry.modify_base(gtk.STATE_NORMAL,
                                                   self.color_white)
                    self.entry.modify_text(gtk.STATE_NORMAL,
                                                   self.color_black)           
        except ValueError:            
            if self.entry != None:
                self.entry.modify_base(gtk.STATE_NORMAL,
                                       self.color_red)
                self.entry.modify_text(gtk.STATE_NORMAL,
                                       self.color_white)
                                       
    #################### Private Methods ####################

    def __get_environment(self):
        """
        This method updates some variables according current document.
        """
        self.view = self.document_manager.get_active_view()
        self.buffer = self.view.buffer
        self.cursor_mark = self.buffer.get_insert()

    def __get_matches(self, string, start_iter, end_iter):
        """
        This method does all the heavy work to find the matches.
        
        @param string: The searched text.
        @type string: A string.
        
        @param start_iter: A iter at the start of current search.
        @type start_iter: A TextIter object.
        
        @param end_iter: A iter at the end of current search.
        @type end_iter: A TextIter object.
        """
        self.matches_num = 0

        begin = start_iter
        end = end_iter
        
        self.buffer.remove_tag_by_name("searchmatch", begin, end)
        
        # If the "search for" field is empty, set normal colors
        if string == "":
            self.matches = None
            self.entry.modify_base(gtk.STATE_NORMAL, self.color_white)
            self.entry.modify_text(gtk.STATE_NORMAL, self.color_black)
            
            if self.entry_replace != None:
                self.entry_replace.modify_base(gtk.STATE_NORMAL,
                                               self.color_white)
                self.entry_replace.modify_text(gtk.STATE_NORMAL,
                                               self.color_black)
            
            return
        
        positions = []
        self.index_cursor = 0
        buffer_text = self.buffer.get_text(begin, end)
        
        # Search operation
        try:
            if self.regexp:
                matches = re.finditer(string, unicode(buffer_text),
                                      re.UNICODE|re.MULTILINE|re.IGNORECASE)
                
            else:
                matches = re.finditer(re.escape(string), unicode(buffer_text),
                                      re.UNICODE|re.MULTILINE|re.IGNORECASE)
        except re.error:
            self.entry.modify_base(gtk.STATE_NORMAL, self.color_red)
            self.entry.modify_text(gtk.STATE_NORMAL, self.color_white)
            
            if self.entry_replace != None:
                self.entry_replace.modify_base(gtk.STATE_NORMAL,
                                               self.color_red)
                self.entry_replace.modify_text(gtk.STATE_NORMAL,
                                               self.color_white)
            return
        
        #Set background color for the matches and store they
        for match in matches:
            match_pos = match.span()
            
            start_iter = self.buffer.get_iter_at_offset(begin.get_offset()
                                                        + match_pos[0])
            stop_iter = self.buffer.get_iter_at_offset(begin.get_offset()
                                                       + match_pos[1])
            
            start = self.buffer.create_mark(None, start_iter)
            stop = self.buffer.create_mark(None, stop_iter)
            
            self.buffer.apply_tag_by_name("searchmatch", start_iter,
                                          stop_iter)
                                          
            # Determine the match closer of the text cursor
            cursor_iter = self.buffer.get_iter_at_mark(self.cursor_mark)
            if start_iter.compare(cursor_iter) < 0:
                self.index_cursor += 1
                
            self.matches_num += 1
            
            positions.append((start, stop))
            
        # If nothing is find, change colors of text field
        if self.matches_num == 0 and self.all_search:
            self.matches = None
            self.entry.modify_base(gtk.STATE_NORMAL, self.color_red)
            self.entry.modify_text(gtk.STATE_NORMAL, self.color_white)
            
            if self.entry_replace != None:
                self.entry_replace.modify_base(gtk.STATE_NORMAL,
                                               self.color_red)
                self.entry_replace.modify_text(gtk.STATE_NORMAL,
                                               self.color_white)
            
        else:
            self.matches = positions
            self.entry.modify_base(gtk.STATE_NORMAL, self.color_white)
            self.entry.modify_text(gtk.STATE_NORMAL, self.color_black)
            
            if self.entry_replace != None:
                self.entry_replace.modify_base(gtk.STATE_NORMAL,
                                               self.color_white)
                self.entry_replace.modify_text(gtk.STATE_NORMAL,
                                               self.color_black)
            
        # If do not exist any match below the cursor....
        if self.index_cursor >= len(positions):
            self.index_cursor = 0
    
