# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2007-2009 Yuri Malheiros.
# Copyright © 2009 TextFlow Team.
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
This module implements a class responsible for manipulate all open documents.
"""

import gtk
import gtksourceview2
import gnomevfs
import gobject
import os
import pango
import gettext

import tf.app
from tf.core import constants
from tf.com.search import Search
from tf.com.modificationmonitor import ModificationMonitor

from tf.document import Document
from tf.widgets.filedialog import SaveFileDialog as SaveFileDialog
from tf.widgets.closealertdialog import CloseAlertDialog
from tf.widgets.errordialog import ErrorDialog
from tf.widgets.changeencodingdialog import ChangeEncodingDialog
from tf.widgets.closebutton import CloseButton

_ = gettext.gettext

class DocumentManager(gtk.Notebook):
    """
    This class has operations to manipulate all documents open.
    """

    __gsignals__ = { "open-file" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                 (Document,)),
                     "save-file" :  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                 (Document,)),
                     "close-file" :  (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                 (Document,))}

    def __init__(self):
        """
        Constructor.
        """
        super(DocumentManager, self).__init__()
        
        #self.interface = interface
        #self.main_window = interface.main_window
        #self.trigger_manager = TriggerManager(self)
        #self.language_manager = LanguageManager()
        self.preferences_manager = tf.app.preferences_manager
        self.trigger_manager = tf.app.trigger_manager
        self.language_manager = tf.app.language_manager
        self.modification_monitor = ModificationMonitor(self)
        
        self.search_functions = Search(self)
        
        self.set_scrollable(True)
        self.connect("switch-page", self.change_tab)
        
        self.__get_color_styles()
        self.doing_sticky = False
        
    
    #################### Public Methods ####################

    def open_tab(self, file_uri="", encode=""):
        """
        Open a new tab.
        
        @param file_uri: The file uri of a text file that will be displayed in the open tab.
                         If it's omited a blank tab will be open.
        @type file_uri: A String.
        
        @param encode: The enconding used to display the text.
                       If it's omited a default enconde will be used.
        @param encode: A String.
        """
        
        if file_uri != "":
            # Verifying if the file is already open
            tab_number = self.get_n_pages()
            for number in range(tab_number):
                if self.get_nth_page(number).file_uri == file_uri:
                    self.set_current_page(number)
                    return
                    
            # defining tab label text
            label_text = os.path.basename(file_uri)
        else:
            label_text = constants.MESSAGE_0001
            
            
        #creating label widget
        tab_box = gtk.HBox(False, 4)
        tab_label = gtk.Label(label_text)
        tab_button = CloseButton()
        
        tab_box.pack_start(tab_label, True, True, 0)
        tab_box.pack_start(tab_button, False, False, 0)
        tab_box.show_all()
        
        try:
            document = self.__create_document(file_uri, encode)
        except UnicodeDecodeError:
            encoding = self.__show_encoding_dialog()

            if encoding is not None:
                self.open_tab(file_uri, encoding)
                
        except IOError:
            self.__show_error_dialog(constants.MESSAGE_0033 % file_uri,
                                     constants.MESSAGE_0034)
            
        else:
            child = self.get_nth_page(0)
            
            if self.get_n_pages() == 1:
                if child.get_file_uri() == "" and child.get_text() == "":
                    if document.get_file_uri() != "":
                        self.__remove_tab(child)
            
            if file_uri != "":
                if self.preferences_manager.get_value("open_save/auto_save"):
                    self.add_to_autosave(document)
            
            self.append_page(document, tab_box)
            self.set_tab_reorderable(document, True)
            self.set_current_page(-1) #negative number == last tab
            tab_button.connect('clicked', self.close_tab_button, document)
            document.view.buffer.connect('changed', self.buffer_change, document, tab_label)
            self.emit("open-file", document)
            
            document.view.grab_focus()

    def close_tab(self, document):
        """
        Close a document tab.
        
        @param document: The document that will be closed.
        @type document: A Document object.
        """
        
        if not isinstance(document, Document):
            raise TypeError("The argument must be a Document object")
        
        if not document.is_updated():
            dialog = CloseAlertDialog()
            button_clicked = dialog.run()
            
            dialog.destroy()
            if button_clicked == gtk.RESPONSE_DELETE_EVENT or \
               button_clicked == 2:
                return
            elif button_clicked == 3:
                self.save_tab(document)
            
        self.remove_from_autosave(document)
        self.__remove_tab(document)
        self.emit("close-file", document)
        
        if self.get_n_pages() == 0:
            self.open_tab()
    
    def save_tab(self, document, show_error=True):
        """
        Save a tab that contains a document.
        
        @param document: A document to save.
        @type document: A Document.
        """
        save_file = document.file_uri
        
        if save_file == "":
            save_file = self.__show_save_file_dialog()
            
            if save_file is None:
                return
        
        self.__save_document(document, save_file, show_error)
        
    def save_as_tab(self, document, show_error=True):
        """
        Ask a filename and save a tab that contains a document.
        
        @param document: a document to save.
        @type document: a Document.
        """
        save_file = self.__show_save_file_dialog()
        
        if save_file is None:
            return
        
        self.__save_document(document, save_file, show_error)
        
    def save_all_tabs(self, show_error=True):
        """
        Save all open documents.
        """
        for document in self:
            self.save_tab(document, show_error)
            
    def save_active_tab(self, show_error=True):
        """
        Save the active document.
        """
        document = self.get_active_document()
        self.save_tab(document, show_error)
    
    def get_active_document(self):
        """
        Get the active Document.
        
        @return: The active Document.
        @rtype: A Document object.
        """
        current_page = self.get_current_page()
        
        if current_page == -1:
            return None
        else:
            return self.get_nth_page(current_page)
    
    def get_active_view(self):
        """
        Get the active GtkSourceView2
        
        @return: The active GtkSourceView2.
        @rtype: A GtkSourceView2 object.
        """
        return self.get_active_document().view
    
    def store_tabs(self):
        """
        Store all open documents. They are reopened using open_stored_tabs
        method or on TextFlow startup if the option 'Reopen tabs on program
        initialization' is true in preferences.
        """
        store_file_uri = os.path.join(constants.HOME, ".textflow", "stored_tabs")
        
        try:
            store_file = open(store_file_uri, "w")
        except IOError:
            self.__show_error_dialog(constants.MESSAGE_0035, constants.MESSAGE_0036)
            return
        
        num_pages = self.get_n_pages()
        
        for i in range(num_pages):
            document = self.get_nth_page(i)
            if document.file_uri != "":
                store_file.write(document.file_uri + "\n" + document.encode + "\n")
        
        store_file.close()
        
    def open_stored_tabs(self):
        #TODO: show error if the stored_tabs file exists but it's impossible to read
        """
        Open tabs saved in stored_tabs file. See the store_tabs method.
        """
        
        store_file_uri = os.path.join(constants.HOME, ".textflow", "stored_tabs")
        
        try:
            store_file = open(store_file_uri, "r")
        except IOError:
            return
        else:
            lines = store_file.readlines()
            cont = 0
            while cont < len(lines):
                try:
                    if os.path.exists(lines[cont][:-1]):
                        self.open_tab(lines[cont][:-1], lines[cont+1][:-1])
                except:
                    pass
                
                # jump 2 lines
                cont += 2
            
    def change_encode(self, document, encode):
        #TODO: this method isn't use the document passed argument
        #TODO: what happen if a invalid encoding is passed?
        """
        Change the text encode of a document.
        
        @param document: a document to change the encoding
        @type document: a Document.
        
        @param encode: encode name.
        @type encode: a String.
        """
        
        page_num = self.get_current_page()
        
        if page_num != -1:
            document = self.get_nth_page(page_num)

            if document.encode != encode:
                file_uri = document.file_uri
                
                if file_uri != "":
                    if not document.is_updated():
                        dialog = CloseAlertDialog()
                        dialog.set_markup(constants.MESSAGE_0014)

                        button_clicked = dialog.run()

                        if button_clicked == gtk.RESPONSE_DELETE_EVENT:
                            dialog.destroy()
                            return
                        elif button_clicked == 1:
                            dialog.destroy()
                        elif button_clicked == 2:
                            dialog.destroy()
                            return
                        elif button_clicked == 3:
                            self.save_active_tab(file_uri)
                           
                            dialog.destroy()
                                                       
                        self.__remove_tab(document)
                        self.open_tab(file_uri, encode)
                    else:
                        self.__remove_tab(document)
                        self.open_tab(file_uri, encode)
                        
                    new_page_num = self.get_current_page()
                    document = self.get_nth_page(new_page_num)
                    self.reorder_child(document, page_num)
    
    def add_to_autosave(self, document):
        """
        Add a document to auto save.
        
        @param document: the document added to auto save.
        @type document: a Document.
        """
        minutes = self.preferences_manager.get_value("open_save/auto_save_minutes")
        document.autosave = gobject.timeout_add(minutes*60000, self.__save_document, document,
                                            document.file_uri, priority=gobject.PRIORITY_LOW)

    def remove_from_autosave(self, document):
        """
        Remove a document from auto save.
        
        @param document: the document added to auto save.
        @type document: a Document.
        """
        if not isinstance(document, Document):
            raise TypeError("The argument must be a Document object")
        
        if document.file_uri != "" and document.autosave:
            gobject.source_remove(document.autosave)
            document.autosave = False

    def set_style(self, view, value):
        """
        Set the color style used by a TFSourceView.
        
        @param view: The TFSourceView.
        @type view: A TFSourceView object.
        
        @param value: A color style name.
        @type value: A string.
        """
        
        scheme = self.style_manager.get_scheme(value)
        buffer = view.buffer
        
        if scheme != None:
            buffer.set_style_scheme(scheme)
            
            style_scheme = buffer.get_style_scheme()
            style = style_scheme.get_style("search-match")
            style_sticky = style_scheme.get_style("def:note")
            
            # Set search match color
            if style != None:
                foreground = style.get_property("foreground")
                background = style.get_property("background")
            else:
                foreground = "black"
                background = "lightblue"

            if style_sticky != None:
                foreground_sticky = style_sticky.get_property("foreground")
                background_sticky = style_sticky.get_property("background")
            else:
                foreground_sticky = "black"
                background_sticky = "#ff6100"
            
            tag_table = buffer.get_tag_table()
            tag = tag_table.lookup("searchmatch")
            tag_sticky = tag_table.lookup("sticky")
            
            if foreground != None:
                tag.set_property("foreground", foreground)
                tag_sticky.set_property("foreground", foreground_sticky)
            else:
                tag.set_property("foreground", "black")
                tag_sticky.set_property("foreground", "black")
            
            if background != None:
                tag.set_property("background", background)
                tag_sticky.set_property("background", background_sticky)
            
    def undo(self):
        """
        Undo a action of current view.
        """
        
        document = self.get_active_document()
        view = document.view
        buffer = view.buffer
        can_undo = buffer.can_undo()
        
        if can_undo:
            buffer.undo()
            
            if buffer.can_redo():
                #self.interface.toolbutton_redo.set_sensitive(True)
                tf.app.main_window.toolbutton_redo.set_sensitive(True)
            
            can_undo = buffer.can_undo()
            
            if not can_undo:
                #self.interface.toolbutton_undo.set_sensitive(False)
                tf.app.main_window.toolbutton_undo.set_sensitive(False)
            
            if document.is_updated():
                child = self.get_nth_page(self.get_current_page())
                label_box = self.get_tab_label(child)
                label = label_box.get_children()[0]
                label.set_label(label.get_label()[1:])
                document.modified = False
     
    def redo(self):
        """
        Redo a action of current view.
        """
        
        view = self.get_active_view()
        buffer = view.buffer
        can_redo = buffer.can_redo()
        
        if view != None and can_redo:
            buffer.redo()
            
            if buffer.can_undo():
                #self.interface.toolbutton_undo.set_sensitive(True)
                tf.app.main_window.toolbutton_undo.set_sensitive(True)
            
            can_redo = buffer.can_redo()
            
            if not can_redo:
                #self.interface.toolbutton_redo.set_sensitive(False)
                tf.app.main_window.toolbutton_redo.set_sensitive(False)
        
    #################### Private Methods ####################
    
    def __get_color_styles(self):
        """
        This method gets all available color styles.
        """
        styles_dir = os.getenv("HOME") + "/.textflow/colors"
        self.style_manager = gtksourceview2.StyleSchemeManager()
        self.style_manager.prepend_search_path(styles_dir)
    
    def __create_document(self, file_uri, encode):
        """
        Create a Document and set some properties.
        
        @param file_uri: A file that will be displayed in TFSourceView.
        @type file_uri: A string
        
        @return: The Document created.
        @rtype: A Document object.
        """
        buffer = gtksourceview2.Buffer()
        pm = self.preferences_manager
        
        #Color stuff
        buffer.create_tag("searchmatch", background="lightblue")
        buffer.create_tag("sticky", background="#ff6100")
        buffer.set_highlight_syntax(True)
        
        document = Document(buffer, file_uri, encode)
        view = document.view
        
        #Getting view language id
        language = view.buffer.get_language()
        
        if language != None:
            language_id = language.get_id()
            self.language_manager.change_mode(language_id)
            language_configs = self.language_manager.loaded_configs[language_id]
            view.set_tab_width(language_configs["tab-size"])
        else:
            self.language_manager.change_mode(None)
            view.set_tab_width(pm.get_value("indentation/tab_width"))
        
        # Define view encode to default encoding 
        if document.encode == "":
            document.encode = pm.get_value("open_save/encoding")
        
        #applying properties
        view.modify_font(pango.FontDescription(pm.get_value("font")))
        view.set_insert_spaces_instead_of_tabs(pm.get_value("indentation/use_spaces"))
        view.set_auto_indent(pm.get_value("indentation/automatic"))
        view.set_show_right_margin(pm.get_value("right_margin/display"))
        view.set_right_margin_position(pm.get_value("right_margin/position"))
        view.set_show_line_numbers(pm.get_value("line_numbers"))
        view.set_highlight_current_line(pm.get_value("highlight_current_line"))
        document.set_text_wrapping(pm.get_value("text_wrapping"))
        view.buffer.set_highlight_matching_brackets(pm.get_value("brackets_matching"))
        view.set_smart_home_end(False)
        self.set_style(view, pm.get_value("color_style"))
        
        view.connect('key-press-event', self.pre_key_press)
        view.connect('key-release-event', self.key_release)
        view.connect("drag-motion", self.drag_motion)
        view.connect("drag-drop", self.drag_drop)
        view.connect("drag-data-received", self.drag_data_received)
        view.drag_dest_set(gtk.DEST_DEFAULT_ALL, [("text/uri-list", 0, 1)],
                           gtk.gdk.ACTION_COPY)
        #view.buffer.connect("notify::cursor-position", self.cursor_moved, document,
        #                    self.interface.statusbar)
                            
        view.buffer.connect("notify::cursor-position", self.cursor_moved, document)
                            
        document.show_all()
        return document
    
    def __remove_tab(self, document):
        """
        Remove a Notebook tab.
        """
        page = self.page_num(document)
        
        if page == -1:
            raise ValueError("Document doesn't exist.")
        
        document.word_complete.stop_indexer()
        self.remove_page(page)
    
    def __show_error_dialog(self, main_text, secondary_text):
        error_dialog = ErrorDialog(main_text, secondary_text)
        button_clicked = error_dialog.run()
        
        if button_clicked == gtk.RESPONSE_DELETE_EVENT:
            error_dialog.destroy()
        elif button_clicked == 1:
            error_dialog.destroy()
    
    def __save_document(self, document, save_file, show_error=True):
        
        try:
            text = document.get_text().encode(document.encode)
        except UnicodeEncodeError:
            self.__show_error_dialog(constants.MESSAGE_0018, constants.MESSAGE_0025)
            return
        
        try:
            arquivo = open(save_file, "w")
        except IOError:
            if show_error:
                document.permission = "Read Only"
                tf.app.main_window.statusbar.permission_label.set_text(document.permission)
                self.__show_error_dialog(constants.MESSAGE_0018, constants.MESSAGE_0019)
        else:
            line_ending = self.preferences_manager.get_value("open_save/line_ending")
            
            if line_ending == "CR LF":
                text = text.replace("\n","\r\n")

            if self.preferences_manager.get_value("open_save/save_copy") == True:
                arquivo_copy = open(save_file + "~", "w")
                arquivo_copy.write(text)                
                arquivo_copy.close()
            
            arquivo.write(text)
            arquivo.close()
            
            if document.file_uri == "":
                if self.preferences_manager.get_value("open_save/auto_save"):
                    self.add_to_autosave(document)
            
            document.set_file_uri(save_file)
                
            #Getting view language id
            language = document.view.buffer.get_language()
            
            if language != None:
                language_id = language.get_id()
                
                if self.language_manager.language != language_id:
                    self.language_manager.change_mode(language_id)
                    language_configs = self.language_manager.loaded_configs[language_id]
                    document.view.set_tab_width(language_configs["tab-size"])
            else:
                self.language_manager.change_mode(None)

            tf.app.main_window.statusbar.combobutton_tab_size.set_label(constants.MESSAGE_0026 + " " + str(document.view.get_tab_width()))
            
            
            current_page = self.page_num(document)
            current_child = self.get_nth_page(current_page)
            tab_label = self.get_tab_label(current_child)
            children = tab_label.get_children()
            
            f_list = save_file.split("/")
            file_name = f_list.pop()
            direc = " (" + "/".join(f_list) + ")"
            
            children[0].set_label(file_name)
            
            tf.app.main_window.main_window.set_title(str(file_name) + direc)
            
            self.emit("save-file", document)

            document.modified = False
            document.permission = "Writable"
            #self.interface.statusbar.permission_label.set_text(document.permission)
            tf.app.main_window.statusbar.permission_label.set_text(document.permission)
            
    def __show_encoding_dialog(self):
        """
        Show the choose encoding dialog
        
        @return: if OK button is pressed - selected encoding.
                 if anything else is done - None.
        @rtype: a String.
        """
        dialog_encoding = ChangeEncodingDialog()
        button_clicked = dialog_encoding.run()
        encoding = None
        
        if button_clicked == gtk.RESPONSE_DELETE_EVENT:
            dialog_encoding.destroy()
        elif button_clicked == 1:
            encoding = dialog_encoding.get_encoding()
            dialog_encoding.destroy()
        elif button_clicked == 2:
            dialog_encoding.destroy()
            
        return encoding
    
    def __show_save_file_dialog(self):
        """
        Show a dialog to choose a filename to save the document.
        
        @return: a filename
        @rtype: a String.
        """
        #file_save = SaveFileDialog(constants.MESSAGE_0002, None,
        #                           "", "*", False, self.interface.last_dir)
        file_save = SaveFileDialog(constants.MESSAGE_0002, None,
                                   "", "*", False, tf.app.main_window.last_dir)
        new_file = file_save.run()
        file_save.destroy()
        
        if len(new_file):
            return new_file[0]
        else:
            return None

    #################### Callbacks ####################

    def close_tab_button(self, widget, document):
        """
        Close a tab in the DocumentManager
        
        @param widget: Reference to the widget.
        @type widget: A widget object.
        
        @param swindow: A Document.
        @type swindow: A Document object.
        """
        self.close_tab(document)
    
    def change_tab(self, widget, page, page_num):
        """
        This method does some operations when tabs are changed.
        """
        previous_document = widget.get_active_document()
        if previous_document != None:
            previous_document.word_complete.stop_indexer()
            
        document = self.get_nth_page(page_num) 
        view = document.view
        
        document.word_complete.start_indexer()
        
        self.search_functions.view = view
        self.search_functions.buffer = view.buffer
        
        self.search_functions.cursor_mark = \
        self.search_functions.buffer.get_insert()
         
        title = document.get_file_uri()
        if title == "":
            file_name = constants.MESSAGE_0001
            direc = ""
        else:
            f_list = title.split("/")
            file_name = f_list.pop()
            direc = " (" + "/".join(f_list) + ")"
        
        #self.main_window.set_title(str(file_name) + direc)
        tf.app.main_window.main_window.set_title(str(file_name) + direc)
        begin = view.buffer.get_start_iter()
        end = view.buffer.get_end_iter()
        self.search_functions.update_matches(begin, end)
        
        pos = document.get_cursor_position()
        
        #Getting view language id
        language = view.buffer.get_language()
        
        if language != None:
            language_id = language.get_id()
            self.language_manager.change_mode(language_id)
        else:
            self.language_manager.change_mode(None)
            
        #self.interface.statusbar.set_line_column(pos[0], pos[1])
        #self.interface.statusbar.combobutton_encoding.set_label(document.encode)
        #self.interface.statusbar.permission_label.set_text(document.permission)
        #self.interface.statusbar.combobutton_tab_size.set_label(constants.MESSAGE_0026 + " " + str(view.get_tab_width()))
        
        tf.app.main_window.statusbar.set_line_column(pos[0], pos[1])
        tf.app.main_window.statusbar.combobutton_encoding.set_label(document.encode)
        tf.app.main_window.statusbar.permission_label.set_text(document.permission)
        tf.app.main_window.statusbar.combobutton_tab_size.set_label(constants.MESSAGE_0026 + " " + str(view.get_tab_width()))
    
    def drag_motion(self, textview, context, x, y, time):
        """
        Handles callback when a drag operation begins.
        """
        
        if "text/uri-list" in context.targets:
            return True
        else:
            return False

    def drag_drop(self, textview, context, x, y, time):
        """
        Handles callback when a drop operation begins.
        """
        if "text/uri-list" in context.targets:
            return True
        else:
            return False
        
    def drag_data_received(self, textview, context, xcord, ycord,
                              selection_data, info, timestamp):
        """
        Handles callback when a drop operation finishes.
        """
        
        if not ("text/uri-list" in context.targets):
            return False
        else:
            if info != 1:
                return False
            
            # Load file
            uri_list = list(selection_data.get_uris())
            
            for i in uri_list:
                filepatch = gnomevfs.get_local_path_from_uri(i)
                if os.path.getsize(filepatch) > 5120000:
                    dialog = gtk.MessageDialog(tf.app.main_window.main_window, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, (constants.MESSAGE_0030) % filepatch)
                    choice = dialog.run()
                    dialog.destroy()                    
                    if choice == gtk.RESPONSE_YES:
                        self.open_tab(filepatch)
                else:
                    self.open_tab(filepatch)
            
            context.finish(True, False, timestamp)
            return True                         
    
    def cursor_moved(self, buffer, position, document):
        pos = document.get_cursor_position()
        #statusbar.set_line_column(pos[0], pos[1])
        tf.app.main_window.statusbar.set_line_column(pos[0], pos[1])
    
    def key_release(self, widget, event):
        """
        This method does some operations when a key is realeased.
        """
        last = self.trigger_manager.last_shortcut
#         print "--------------------------"
        #print event.state
        #print event.keyval
#         print "--------------------------"
        if last in self.trigger_manager.sticky_keys:
            if event.state & gtk.gdk.CONTROL_MASK and event.state & gtk.gdk.SHIFT_MASK:
                pass
#                 print "ctrl+shift+" + unichr(event.keyval).lower()
            elif event.state & gtk.gdk.CONTROL_MASK:
                if "ctrl" in last and (event.keyval == 65507 or not (unichr(event.keyval) in self.trigger_manager.sticky_keys[last])):
                    try:
                        self.trigger_manager.sticky_shortcuts[last]()
                    #except KeyError:
                    #    return
                    finally:
                        self.trigger_manager.last_shortcut = None
                        self.doing_sticky = False
    #         elif event.state & gtk.gdk.SHIFT_MASK:
    #             shortcut = "shift+" + unichr(event.keyval).lower()
    #             shortcut2 = unichr(event.keyval).lower()
    #             if shortcut in self.trigger_manager.sticky_shortcuts:
    #                 self.trigger_manager.sticky_shortcuts[shortcut]()
    #             elif shortcut2 in self.trigger_manager.sticky_shortcuts:
    #                 self.trigger_manager.sticky_shortcuts[shortcut2]()
            else:
                shortcut = unichr(event.keyval).lower()
                last_key = last.split("+")[-1]
                if shortcut == last_key:
                    try:
                        self.trigger_manager.sticky_shortcuts[last]()
                    #except KeyError:
                    #    return
                    finally:
                        self.trigger_manager.last_shortcut = None
                        
        view = self.get_active_view()
        view.scroll_mark_onscreen(view.buffer.get_insert())
        
    def pre_key_press(self, widget, event):
        #print event.keyval
        #print event.state
        
        if self.doing_sticky:
            return False
        
        if event.state & gtk.gdk.CONTROL_MASK \
        and event.state & gtk.gdk.SHIFT_MASK:
            shortcut = "ctrl+shift+" + unichr(event.keyval).lower()
            if shortcut in self.trigger_manager.shortcuts:
                r = self.trigger_manager.shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut in self.trigger_manager.language_shortcuts:
                r = self.trigger_manager.language_shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            else:
                return False
        elif event.state & gtk.gdk.CONTROL_MASK:
            shortcut = "ctrl+" + unichr(event.keyval).lower()
            if shortcut in self.trigger_manager.shortcuts:
                r = self.trigger_manager.shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut in self.trigger_manager.language_shortcuts:
                r = self.trigger_manager.language_shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            else:
                return False
        elif event.state & gtk.gdk.SHIFT_MASK:
            shortcut = "shift+" + unichr(event.keyval).lower()
            shortcut2 = unichr(event.keyval).lower()
            if shortcut in self.trigger_manager.shortcuts:
                r = self.trigger_manager.shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut2 in self.trigger_manager.shortcuts:
                r = self.trigger_manager.shortcuts[shortcut2]()
                self.trigger_manager.last_shortcut = shortcut2
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut in self.trigger_manager.language_shortcuts:
                r = self.trigger_manager.language_shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut2 in self.trigger_manager.language_shortcuts:
                r = self.trigger_manager.language_shortcuts[shortcut2]()
                self.trigger_manager.last_shortcut = shortcut2
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            else:
                return False
        else:
            
            #print self.trigger_manager.language_shortcuts
            shortcut = unichr(event.keyval).lower()
                        
            if shortcut in self.trigger_manager.shortcuts:
                r = self.trigger_manager.shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            elif shortcut in self.trigger_manager.language_shortcuts:
                r = self.trigger_manager.language_shortcuts[shortcut]()
                self.trigger_manager.last_shortcut = shortcut
                
                if shortcut in self.trigger_manager.sticky_shortcuts:
                    self.doing_sticky = True
                
                return r
            else:
                return False
        
    def buffer_change(self, widget, document, label):
        if not document.modified:
            text = label.get_text()
            document.modified = True
            label.set_text("*" + text)
        
        #toolbutton_undo = self.interface.toolbutton_undo 
        #toolbutton_redo = self.interface.toolbutton_redo
         
        toolbutton_undo = tf.app.main_window.toolbutton_undo 
        toolbutton_redo = tf.app.main_window.toolbutton_redo 
        
        if document.view.buffer.can_undo():
            if not toolbutton_undo.get_property("sensitive"):
                #self.interface.toolbutton_undo.set_sensitive(True)
                tf.app.main_window.toolbutton_undo.set_sensitive(True)
        
        if not document.view.buffer.can_redo():
            if toolbutton_redo.get_property("sensitive"):
                #self.interface.toolbutton_redo.set_sensitive(False)
                tf.app.main_window.toolbutton_redo.set_sensitive(False)
        
        self.search_functions.all_search = False
        start, end = document.get_line_iters()
        self.search_functions.update_matches(start, end)
