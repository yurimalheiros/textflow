# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2008 Yuri Malheiros.
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
This module implements a class responsible for creating the TFSourceView.
"""

import gtk
import gtksourceview2
import gnomevfs
import os

import tf.app
from tf.com.snippetmanager import SnippetManager
from tf.com.wordcomplete import WordComplete
from tf.widgets.notifier import Notifier
import tf.com.files as Files

class Document(gtk.VBox):
    """
    This class implements the Document widget.
    """
    
    def __init__(self, buffer, file_uri="", encode=""):
        """
        Constructor.
        
        @param buffer: The SourceBuffer of this view.
        @type buffer: A SourceBuffer object.
        
        @param file_uri: The file that will be opened in this view.
        @type file_uri: A string.
        """
        super(Document, self).__init__()
        self.buffer = buffer
        self.view = gtksourceview2.View(buffer)
        self.view.buffer = buffer
        self.file_uri = file_uri
        self.modified = False
        self.encode = encode
        self.snippets = SnippetManager(self)
        self.word_complete = WordComplete(self)
        self.__notifier = Notifier()
        self.autosave = False
        self.permission = "Writable"
        
        if self.file_uri != "":
            #Verify permission
            #file_info = gnomevfs.get_file_info(file_uri)
            if not (os.access(file_uri, os.W_OK)):
                self.permission = "Read only"
            
            self.buffer.begin_not_undoable_action()
            
            current_file = open(file_uri, "r")
            file_text = current_file.read()
            self.set_text(file_text, encode)
            
            self.buffer.end_not_undoable_action()
            self.buffer.place_cursor(self.buffer.get_start_iter())
            current_file.close()
            
            self.__set_language(file_uri)
            self.word_complete.indexer()
        
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.add(self.view)
        self.pack_start(self.scrolled_window)
        self.pack_start(self.__notifier, False, False)
        
        self.revert_button = gtk.Button()
        revert_image = gtk.Image()
        revert_image.set_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_MENU)
        self.revert_button.add(revert_image)
        
        self.__notifier.custom_widget = self.revert_button
        
        self.revert_button.connect("clicked", self.revert_clicked)
        self.__notifier.connect("close-clicked", self.notifier_close)
            
    #################### Public Methods ####################
            
    def get_file_uri(self):
        """
        Get the uri of the file opened in this view.
        
        @return: The uri of the file opened in this view.
        @rtype: A string.
        """
        return self.file_uri
        
    def set_file_uri(self, new_file_uri):
        """
        Set the uri of the file opened in this view.
        
        @param new_file_uri: The new uri of the file opened.
        @type file_uri: A string.
        """
        self.file_uri = new_file_uri
        self.__set_language(new_file_uri)
        
    def set_text(self, text, encode=""):
        if encode != "":
            text = unicode(text, encode)
        elif self.encode != "":
            text = unicode(text, self.encode)
        else:
            pm = tf.app.preferences_manager
            default_encoding = pm.get_value("open_save/encoding")
            text, encoding = Files.guess_encoding(text, default_encoding)
            self.encode = encoding
        
        self.buffer.set_text(self.__process_text(text))
        
    def get_text(self):
        """
        Get the text of the active view.
        
        @return: The text of the active view.
        @rtype: A string.
        """
        return self.buffer.get_text(self.buffer.get_start_iter(),
                                    self.buffer.get_end_iter(), True)
                                    
    def get_line_iters(self):
        """
        Get the iter at the start and at the end of a current line.
        
        @return: the iter at the start and the iter at the end of current line
        @rtype: A tuple.
        """
        buffer = self.buffer
        
        start_iter = buffer.get_iter_at_mark(buffer.get_insert())
        line_num = start_iter.get_line()
        end_iter = start_iter.copy()
        
        if not end_iter.ends_line():
            end_iter.forward_to_line_end()
        start_iter = buffer.get_iter_at_line(line_num)
        
        return (start_iter, end_iter)
    
    def get_indentation(self, insert_iter):
        """
        This method gets the current line indentation
        
        @param insert_iter: The insert cursor iter.
        @type insert_iter: A TextIter object.
        
        @return: A string of characters (tabs and/or spaces)
        @rtype: A string.
        """
        buffer = self.buffer
        line_num = insert_iter.get_line()
        line_iter = buffer.get_iter_at_line(line_num)
        indent = []
        while True:
            char = line_iter.get_char()
            if char == " " or char == "\t":
                line_iter.forward_char()
                indent.append(char)
            else:
                break
        indent = "".join(indent)
        
        return indent
    
    def get_cursor_position(self):
        cursor_mark = self.buffer.get_insert()
        cursor_iter = self.buffer.get_iter_at_mark(cursor_mark)
        
        cursor_line = cursor_iter.get_line()
        start_iterator = self.buffer.get_iter_at_line(cursor_line)

        line_text = self.buffer.get_text(start_iterator, cursor_iter)
        tabs_width = self.view.get_tab_width()
        count = 0
        
        for characters in line_text:
            if characters == "\t":
                count += (tabs_width - (count % tabs_width))
            else:
                count += 1
        cursor_column = count
        
        return cursor_line+1, cursor_column+1
    
    def is_updated(self):
        """
        Verify if the file is updated.
        """
        view_text = self.get_text()
        
        if self.file_uri == "":
            if view_text == "":
                return True
            else:
                return False
        else:
            try:
                current_file = open(self.file_uri, "r")
            except IOError:
                return False
            file_text = current_file.read()

            text = unicode(file_text, self.encode)
            text = self.__process_text(text)
            
            current_file.close()
            
            if view_text == text:
                return True
            else:
                return False
                
    def set_text_wrapping(self, value):
        """
        Enable or disable text wrapping in a SourceView.
        
        @param value: True to enable text wrapping and False to disable.
        @type value: A boolean.
        """
        if value:
            self.view.set_wrap_mode(gtk.WRAP_WORD)
        else:
            self.view.set_wrap_mode(gtk.WRAP_NONE)
            
    def notify(self, text):
        self.__notifier.label = text
        self.__notifier.show_all()
        
    def revert(self):
        current_file = open(self.file_uri, "r")
        file_text = current_file.read()
        self.set_text(file_text, self.encode)
        
    def show_all(self):
        self.show()
        self.scrolled_window.show_all()
        
    #################### Private Methods ####################
    
    def __set_language(self, file_uri):
        lm = gtksourceview2.LanguageManager()
        lang_id = Files.get_language_from_mime(gnomevfs.get_mime_type(file_uri))
        
        if lang_id != None:
            language = lm.get_language(lang_id)
            self.snippets.load(lang_id)
            self.buffer.set_language(language)
            
    def __process_text(self, text):
        return text.replace("\r","").replace('\0', '')
            
    #################### Callbacks ####################
    
    def notifier_close(self, notifier):
        self.__notifier.hide()
    
    def revert_clicked(self, button):
        self.revert()
        self.__notifier.hide()
