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
This module implements a class that represents a snippet.
"""

import gtk
import re
import xml.dom.minidom
import xml.parsers.expat
import tf.app
from tf.com.snippet import Snippet
from tf.com.snippetfield import SnippetField
from tf.com.snippetmirror import SnippetMirror
from tf.com.snippetinfo import SnippetInfo
from tf.com.tree import Tree
from tf.widgets.snippetpopupwindow import SnippetPopupWindow
from tf.core import constants

class SnippetManager(object):
    """
    This class manage all snippets of current language.
    """
    def __init__(self, document):
        """
        Constructor.
        
        @param document: The current Document
        @type document: A Document object.
        """
        self.document = document
        self.view = document.view
        self.snippets = {}
        self.language = None
        self.stack = []
        self.top = None
    
    #################### Public Methods ####################
    
    def load(self, language):
        """
        Loads all snippets of current language syntax highlight.
        
        @param language: The name of a language.
        @type language: A string.
        """
        self.language = language
        try:
            doc = \
            xml.dom.minidom.parse(constants.LANGUAGES_USER_DIR + "/" + self.language + "/" + "snippets.xml")
        except IOError:
            self.snippets = {}
        except xml.parsers.expat.ExpatError:
            self.__show_error_dialog()
            self.snippets = {}
        else:
            key = None
            string = None
            name = None
            
            for i in doc.getElementsByTagName("snippet"):
                for node in i.getElementsByTagName("key"):
                    key = node.childNodes[0].data

                for node in i.getElementsByTagName("body"):
                    string = node.childNodes[0].data
                    
                for node in i.getElementsByTagName("name"):
                    name = node.childNodes[0].data

                if key and string and name:
                    info = SnippetInfo(key, string, name)
                    
                    if self.snippets.has_key(key):
                        self.snippets[key].append(info)
                    else:
                        self.snippets[key] = [info]
                else:
                    self.__show_error_dialog()
                    self.snippets = {}
                    return

    def active(self):
        """
        This method actives a snippet.
        
        @param key: The snippet activation key.
        @type: A string.
        """
        if len(self.snippets) == 0:
            return False
        
        buffer = self.view.buffer
        key = self.__get_key()
        
        if self.snippets.has_key(key):
            if len(self.snippets[key]) > 1:
                self.popup_list(key)
                self.id_key_press = self.view.connect('key-press-event',
                                                      self.key_press)
                self.id_event_after = self.view.connect('event-after',
                                             self.event_after, key, self.snippets[key])
                self.id_button_press = self.pw.treeview.connect('event-after',
                                                                self.item_clicked)
                notebook = self.view.get_parent().get_parent().get_parent()
                self.id_switch_page = notebook.connect('switch-page',
                                                       self.switch_page)
            else:
                # Delete key
                insert_mark = buffer.get_insert()
                insert_iter = buffer.get_iter_at_mark(insert_mark)
                start_iter = insert_iter.copy()

                self.__find_word_start(start_iter)
                        
                start_del_mark = buffer.create_mark(None, start_iter, True)
                
                si = buffer.get_iter_at_mark(start_del_mark)
                ei = buffer.get_iter_at_mark(insert_mark)
                buffer.delete(si, ei)
                
                text = self.snippets[key][0].string
                self.__parser(text)
            
            return True
        else:
            return False

    def popup_list(self, key):
        """
        This method popups a window with a list of snippets.
        
        @param key: A snippet key.
        @type key: A string.
        """
        buffer = self.view.buffer
        insert_mark = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert_mark)
        alloc = self.view.get_iter_location(insert_iter)
        cursor_pos = self.view.buffer_to_window_coords(gtk.TEXT_WINDOW_TEXT, 
                                                       alloc.x, alloc.y)
        
        window = self.view.get_window(gtk.TEXT_WINDOW_WIDGET)
        wp_x, wp_y = window.get_origin()
        view_rec = self.view.get_visible_rect()
        position_x = cursor_pos[0] + wp_x + 20
        position_y = cursor_pos[1] + wp_y + 20
        
        if (position_x + 190) > (wp_x + view_rec.width):
            position_x = (wp_x + view_rec.width) - 190
        if (position_y + 190) > (wp_y + view_rec.height):
            position_y = (wp_y + cursor_pos[1]) - 190
            
        self.pw = SnippetPopupWindow()
        self.pw.run(self.snippets[key], (position_x, position_y))
            
    
    def pop_snippet(self):
        """
        Pop a snippet.
        """
        self.stack[-1].remove_marks()
        self.stack.pop()
        
    def push_snippet(self, snippet):
        """
        Push a snippet.
        
        @param snippet: A snippet that will be pushed.
        @type: A Snippet Object.
        """
        self.stack.append(snippet)
    
    def next_field(self):
        """
        This method selects the next field of the snippet at the top of the
        stack.
        """
        self.stack[-1].next()
        
    def previous_field(self):
        """
        This method selects the previous field of the snippet at the top of the
        stack.
        """
        self.stack[-1].previous()
    
    def valid_cursor_position(self):
        """
        This method verify if the insert cursor is between the snippet bounds.
        
        @return: True if insert cursor is between the snippet bounds,
        else, return False.
        @rtype: A boolean.
        """
        buffer = self.view.buffer
        insert = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert)
        begin, end = self.stack[-1].bounds
        begin_iter = buffer.get_iter_at_mark(begin)
        end_iter = buffer.get_iter_at_mark(end)
        
        return insert_iter.in_range(begin_iter, end_iter)


    #################### Signals ####################
    
    def item_clicked(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                buffer = self.view.buffer
                key = self.__get_key()
                position = self.pw.get_selected()
                
                insert_mark = buffer.get_insert()
                insert_iter = buffer.get_iter_at_mark(insert_mark)
                start_iter = insert_iter.copy()

                self.__find_word_start(start_iter)
                        
                start_del_mark = buffer.create_mark(None, start_iter, True)
                
                si = buffer.get_iter_at_mark(start_del_mark)
                ei = buffer.get_iter_at_mark(insert_mark)
                buffer.delete(si, ei)
                
                text = self.snippets[key][position].string
                self.__parser(text)
                
                self.__destroy()
        else:
            return
    
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
        
    def event_after(self, widget, event, key, words):
        if event.type == gtk.gdk.KEY_RELEASE:
            keyval = event.keyval
            
            if keyval == gtk.keysyms.Up:
                return
            elif keyval == gtk.keysyms.Down:
                return
            elif keyval == gtk.keysyms.Return:
                buffer = self.view.buffer
                position = self.pw.get_selected()
                
                insert_mark = buffer.get_insert()
                insert_iter = buffer.get_iter_at_mark(insert_mark)
                start_iter = insert_iter.copy()

                self.__find_word_start(start_iter)
                        
                start_del_mark = buffer.create_mark(None, start_iter, True)
                
                si = buffer.get_iter_at_mark(start_del_mark)
                ei = buffer.get_iter_at_mark(insert_mark)
                buffer.delete(si, ei)
                
                text = self.snippets[key][position].string
                self.__parser(text)
                
                self.__destroy()
            elif keyval == gtk.keysyms.Tab:
                return
            else:
                self.__destroy()
            
            return False
        elif event.type == gtk.gdk.BUTTON_RELEASE:
            self.__destroy()
            return
        else:
            return
            
    def switch_page(self, widget, page, page_num):
        self.__destroy()
    
    #################### Private Methods ####################
    
    def __parser(self, text):
        """
        This method parses the TextFlow snippet definition syntax.
        
        @param text: The text coded using TextFlow snippet definition syntax.
        @type text: A string.
        """
        buffer = self.view.buffer
        
        # Snippet components
        fields = Tree()
        mirrors = []
        stop = None
        
        root_init = fields.add(None, None) #empty root
        root = root_init
        
        # Cursor
        insert = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert)
        
        # Indentation stuff
        pref_manager = tf.app.preferences_manager
        spaces = pref_manager.get_value("indentation/use_spaces")
        tab_width = self.view.get_tab_width()
        indent = self.document.get_indentation(insert_iter)
        
        # Create a mark at start of snippet
        begin_bound_mark = buffer.create_mark(None, insert_iter, True)
        
        # Parsing text
        i = 0
        stack = []
        while (i<len(text)):
            char = text[i]
            
            # Verifying escape char "\"
            if char == "\\":
                self.view.buffer.insert_at_cursor(text[i+1])
                i += 2
                continue            
            
            # Look for a snippet special component "${}"
            if char == '$' and (i+1) < len(text) and text[i+1] == '{':
                
                if text[i+2] == '0':
                    # STOP
                    stop_iter = buffer.get_iter_at_mark(buffer.get_insert())
                    stop = buffer.create_mark(None, stop_iter, True)

                    i += 3
                elif text[i+2] == "%":
                    # MIRROR
                    mirror_iter = buffer.get_iter_at_mark(buffer.get_insert())
                    begin_mark = buffer.create_mark(None, mirror_iter, True)
                    end_mark = buffer.create_mark(None, mirror_iter, True)
                    
                    #begin_mark.set_visible(True)
                    
                    # Get mirror number
                    j = i+3
                    num = []

                    while char != '}' and char != '/':
                        char = text[j]
                        num.append(char)
                        j += 1

                    mirror_num = int("".join(num[:-1]))
                    i = j-1
                    
                    if char == '/':
                        k = i
                        brace_count = 1
                        
                        while True:
                        
                            if text[k] == '{':
                                brace_count += 1
                            elif text[k] == '}':
                                brace_count -= 1
                                
                            if brace_count == 0:
                                break
                                
                            k += 1
                        
                        regexp = text[i+1:k].split('/')
                        i = k
                        
                        m = SnippetMirror(self.view, mirror_num, 
                                      (begin_mark, end_mark))
                        
                        m.regexp = (regexp[0], regexp[1])
                    
                    else:
                        m = SnippetMirror(self.view, mirror_num, 
                                          (begin_mark, end_mark))
                    mirrors.append(m)
                else:
                    # FIELD
                    j = i+2
                    num = []
                    
                    char = text[j]
                    while char != ':':
                        num.append(char)
                        j+=1
                        char = text[j]

                    num = int("".join(num))
                    
                    field_iter = buffer.get_iter_at_mark(buffer.get_insert())
                    begin_mark = buffer.create_mark(None, field_iter, True)
                    #begin_mark.set_visible(True)
                    
                    f = SnippetField(self.view, num, (begin_mark,))
                    
                    root = fields.add(f, root)
                    stack.append(root)

                    i = j
                    
            elif char == '}':
                if len(stack) > 0:
                    node = stack.pop()
                    
                    if len(stack) == 0:
                        root = root_init
                    
                    bm = node.elem.marks[0]
                    end_iter = buffer.get_iter_at_mark(buffer.get_insert())
                    em = buffer.create_mark(None, end_iter, True)
                    #em.set_visible(True)
                    node.elem.marks = (bm, em)

                elif len(stack) == 0:
                    root = root_init
                    self.view.buffer.insert_at_cursor(char)
                else:
                    root = stack[-1]

            elif char == '\t':
                if spaces:
                    self.view.buffer.insert_at_cursor(" " * tab_width)
                else:
                    self.view.buffer.insert_at_cursor(char)
            elif char == '\n':
                # LINE BREAK
                buffer.insert_at_cursor("\n")
                buffer.insert_at_cursor(indent)
            else:
                self.view.buffer.insert_at_cursor(char)
            
            i+=1
        
        #Not well-formed snippet
        if len(stack) > 0:
            fields.pre_order(self.__disconnect_field_signal)
            return
            
        # Change stop gravity
        if stop != None:
            stop_iter = buffer.get_iter_at_mark(stop)
            buffer.delete_mark(stop)
            stop = buffer.create_mark(None, stop_iter, False)
            #stop.set_visible(True)
            
        # Change mirrors gravity
        for i in range(len(mirrors)):
            m = mirrors[i].marks[1]
            n = mirrors[i].marks[0]
            m_iter = buffer.get_iter_at_mark(m)
            buffer.delete_mark(m)
            new_m = buffer.create_mark(None, m_iter, False)
            #new_m.set_visible(True)
            mirrors[i].marks = (n, new_m)
            
        # Change fields gravity
        fields.pre_order(self.__fields_change_gravity)
        
        # Change begin bound gravity
        m = begin_bound_mark
        m_iter = buffer.get_iter_at_mark(m)
        buffer.delete_mark(m)
        begin_bound_mark = buffer.create_mark(None, m_iter, False)
        #begin_bound_mark.set_visible(True)
        
        # Create end bound mark
        insert_iter = buffer.get_iter_at_mark(insert)
        end_bound_mark = buffer.create_mark(None, insert_iter, False)
        #end_bound_mark.set_visible(True)
        
#        print "root: ", fields.root
#        print "root's children: ", fields.root.children
        
        bounds = (begin_bound_mark, end_bound_mark)
        snippet = Snippet(self.document, fields, mirrors, stop, bounds)
        self.push_snippet(snippet)
        
        if len(snippet.fields.root.children) > 0:
            buffer.place_cursor(buffer.get_iter_at_mark(begin_bound_mark))
            self.next_field()
        else:
            self.pop_snippet()
        
    def __fields_change_gravity(self, node):
        """
        This method change gravity of a snippet field's right mark.
        
        @param node: A snippet field.
        @type node: A TreeNode.
        """
        buffer = self.view.buffer
        field = node.elem
        
        if field != None:
            m = field.marks[1]
            n = field.marks[0]
            
            m_iter = buffer.get_iter_at_mark(m)
            buffer.delete_mark(m)
            new_m = buffer.create_mark(None, m_iter, False)
            #new_m.set_visible(True)
            field.marks = (n, new_m)
            
    def __disconnect_field_signal(self, node):
        """
        Disconnect all field's signals.
        
        @param node: A snippet field. 
        @type node:  A TreeNode.
        """
        field = node.elem
        if field != None:
            if field.id != None:
                field.view.disconnect(field.id)
                
    def __show_error_dialog(self):
        """
        Show the snippet error dialog.
        """
        dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR,
                                   gtk.BUTTONS_NONE, None)
        dialog.format_secondary_text(constants.MESSAGE_0012)
        dialog.set_markup(constants.MESSAGE_0011)
        dialog.add_button(gtk.STOCK_OK, 1)
        dialog.run()
        dialog.destroy()

    def __get_key(self):
        """
        Get the snippet key from textbuffer according cursor position.
        """
        buffer = self.view.buffer
        insert_mark = buffer.get_insert()
        insert_iter = buffer.get_iter_at_mark(insert_mark)
        start_iter = insert_iter.copy()

        self.__find_word_start(start_iter)
        key = buffer.get_text(start_iter, insert_iter)
        
        return key
    
    def __find_word_start(self, iterator):
        """
        Find the start of a word.
        
        @param iterator: A iterator at end of a word.
        @type iterator: A TextIter.
        """
        pattern = re.compile("[a-z|A-Z|0-9|<|>|/]")
        symbols = ('!', '@', '#', '$', '%', '&', '*',
                   '(', ')', '-' ,'+', '.', ',', '~', '^')
        iterator.backward_char()
        if iterator.get_char() in symbols:
            return
        while True:
            char = iterator.get_char()
            if not(re.match(pattern, char)):
                iterator.forward_char()
                return
            elif iterator.starts_line():
                return
            else:
                iterator.backward_char()

    def __destroy(self):
        """
        Destroy the snippet popup window.
        """
        self.view.disconnect(self.id_event_after)
        self.view.disconnect(self.id_key_press)

        notebook = self.view.get_parent().get_parent().get_parent()
        notebook.disconnect(self.id_switch_page)
        
        self.pw.destroy()
        self.pw = None
