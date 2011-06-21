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
This module implements a class responsible for word completion.
"""

import gtk
import gobject
import re

from tf.widgets.wordcompletewindow import WordCompleteWindow

class WordComplete(object):
    """
    This class manage word completion operations for a SourceView.
    """
    
    def __init__(self, document):
        """
        Constructor.
        
        @param document: A Document managed by this object.
        @type document: A Document.
        """
        self.view = document.view
        self.buffer = self.view.buffer
        self.words = None
        self.pw = None
        self.indexer_id = None
    
    #################### Public Methods ####################
        
    def get_completions(self, incomplete_word, words=None):
        """
        This method get completions available for a incomplete word.
        
        @param incomplete_word: A incomplete word.
        @type incomplete_word: A string.
        
        @param words: A set of words.
        @type words: A list of strings.
        """
        if self.words == None:
            return []
        
        if words == None:
            words = self.words

        match_list = [list(items) for items in self.words.items() \
        if items[0].startswith(incomplete_word) and  items[0] != incomplete_word]
        
        match_list.sort(self.__sort_matches_occurrence_only)
        matches = [items[0] for items in match_list]
        return matches
                
    def indexer(self):
        """
        Index words of the buffer.
        """
        re_non_alpha = re.compile(r"\W+", re.UNICODE | re.MULTILINE)
        text = unicode(self.buffer.get_text(*self.buffer.get_bounds()))
        
        self.words = re_non_alpha.split(text)
        
        words_unique = self.__remove_duplicate_items(self.words)
        
        self.words = words_unique

        return True
    
    def complete(self, key):
        """
        Complete a word.
        
        @param key: A incomplete word.
        @type key: A string.
        """
        words = self.get_completions(key)
        
        if len(words) == 1:
            self.buffer.insert_at_cursor(words[0][len(key):])
        elif len(words) > 1:
            self.popup_list(key, words)
            self.id_key_press = self.view.connect('key-press-event',
                                                  self.key_press)
            self.id_event_after = self.view.connect('event-after',
                                         self.event_after, key)
            self.id_button_press = self.pw.treeview.connect('event-after',
                                                            self.item_clicked)
            notebook = self.view.get_parent().get_parent().get_parent()
            self.id_switch_page = notebook.connect('switch-page',
                                                   self.switch_page)
            
    def stop_indexer(self):
        """
        Stop the indexer.
        """
        if self.indexer_id != None:
            gobject.source_remove(self.indexer_id)
        
    def start_indexer(self):
        """
        Start the indexer.
        """
        self.indexer_id = gobject.timeout_add(800, self.indexer,
                                              priority=gobject.PRIORITY_LOW)
    
    def popup_list(self, key, words):
        """
        Popup a list of words.
        """
        position_x , position_y = self.__position_window(words)
        
        self.pw = WordCompleteWindow()
        self.pw.run(words, (position_x, position_y))
        
    #################### Signals ####################
    
    def key_press(self, widget, event):
        keyval = event.keyval
        if keyval == gtk.keysyms.Down:
            self.pw.item_down()
            return True
        elif keyval == gtk.keysyms.Up:
            self.pw.item_up()
            return True
        elif keyval == gtk.keysyms.Return:
            return True
        
    def event_after(self, widget, event, key):
        if event.type == gtk.gdk.KEY_RELEASE:
            keyval = event.keyval
            
            key_tam = len(key)
            
            ilegal_keys = (gtk.keysyms.Tab, gtk.keysyms.Right, gtk.keysyms.Left,
                           gtk.keysyms.Home, gtk.keysyms.End, gtk.keysyms.Insert, 
                           gtk.keysyms.Delete, gtk.keysyms.Page_Up,
                           gtk.keysyms.Page_Down, gtk.keysyms.Escape)
            
            if keyval in ilegal_keys:
                self.__destroy()
            elif keyval == gtk.keysyms.Up:
                return
            elif keyval == gtk.keysyms.Down:
                return
            elif keyval == gtk.keysyms.Return:
                new_key = self.__get_key()
                word = self.pw.get_selected()
                self.buffer.insert_at_cursor(word[len(new_key):])
                self.__destroy()
            else:
                new_key = self.__get_key()
                if len(new_key) < key_tam:
                    self.__destroy()
                else:    
                    new_words = self.get_completions(new_key)
                    
                    if len(new_words) == 0:
                        self.__destroy()
                    else:
                        pos_x , pos_y = self.__position_window(new_words)
                        self.pw.update_list(new_words)
                        self.pw.move(pos_x, pos_y)
            return False
        elif event.type == gtk.gdk.BUTTON_RELEASE:
            self.__destroy()
            return
        else:
            return
            
    def item_clicked(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                new_key = self.__get_key()
                word = self.pw.get_selected()
                self.buffer.insert_at_cursor(word[len(new_key):])
                self.__destroy()
        else:
            return
    
    def switch_page(self, widget, page, page_num):
        self.__destroy()
    
    def __destroy(self):
        self.view.disconnect(self.id_event_after)
        self.view.disconnect(self.id_key_press)
        self.view.get_parent().get_parent().get_parent().disconnect(self.id_switch_page)
        self.pw.destroy()
        self.pw = None
    
    #################### Private Methods ####################
    
    def __position_window(self, words):
        insert_mark = self.buffer.get_insert()
        insert_iter = self.buffer.get_iter_at_mark(insert_mark)
        alloc = self.view.get_iter_location(insert_iter)
        cursor_pos = self.view.buffer_to_window_coords(gtk.TEXT_WINDOW_TEXT, 
                                                       alloc.x, alloc.y)
        
        window = self.view.get_window(gtk.TEXT_WINDOW_WIDGET)
        wp_x, wp_y = window.get_origin()
        view_rec = self.view.get_visible_rect()
        position_x = cursor_pos[0] + wp_x + 20
        position_y = cursor_pos[1] + wp_y + 20
        
        if (position_x + 187) > (wp_x + view_rec.width):
            position_x = (wp_x + view_rec.width) - 187
        if (position_y + 187) > (wp_y + view_rec.height):
            position_y = (wp_y + cursor_pos[1]) - 187
            words_size = len(words)
            if words_size < 7:
                position_y += (7 - len(words))*25
        
        return (position_x, position_y)
    
    def __get_key(self):
        insert_mark = self.buffer.get_insert()
        insert_iter = self.buffer.get_iter_at_mark(insert_mark)
        iterator = insert_iter.copy()
    
        pattern = re.compile("[a-z|A-Z|0-9|_]")
        symbols = ('!', '@', '#', '$', '%', '&', '*',
                   '(', ')', '-', '+', '.', ',', '~', '^')
        iterator.backward_char()
        if iterator.get_char() in symbols:
            return iterator.get_char()
        while True:
            char = iterator.get_char()
            if not(re.match(pattern, char)):
                iterator.forward_char()
                break
            elif iterator.starts_line():
                break
            else:
                iterator.backward_char()
        
        key = self.buffer.get_text(iterator, insert_iter)
        return key
    
    def __remove_duplicate_items(self, seq): 
        """
        Remove duplicate items in a list.
        
        @param seq: A list. 
        @type seq: A list.
        """
        unique = {}

        for item in seq:
            if item in unique:
                unique[item] += 1
                continue
            unique[item] = 1
            
        return unique
        
    def __sort_matches_occurrence_only(self, x, y):
        if x[1] < y[1]:
            return 1
        if x[1] > y[1]:
            return -1
        return 0
        
