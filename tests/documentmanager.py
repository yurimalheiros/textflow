import unittest
import os
import gtksourceview2

import tf.app
from tf.core import constants
from tf.document import Document

class DocumentManager(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = tf.app.document_manager
        
        self.testfilename = "testfile"
        self.testfilepath = os.path.join(os.getcwd(), self.testfilename)
        
        self.__remove_all_tabs()
        
    def tearDown(self):
        if os.path.exists(self.testfilepath):
            os.remove(self.testfilepath)
    
    def __remove_all_tabs(self):
        for i in range(len(self.document_manager)):
            self.document_manager.remove_page(-1)
        
    def test_one_blank_tab_open_open_blank_tab(self):
        self.document_manager.open_tab()
        self.document_manager.open_tab()
        
        self.assertEquals(2, len(self.document_manager))
        
    def test_one_blank_tab_open_open_file_tab(self):
        self.document_manager.open_tab()
        new_file = open(self.testfilepath, "w")
        new_file.close()
        self.document_manager.open_tab(self.testfilepath)
        
        self.assertEquals(1, len(self.document_manager))
        
    def test_open_tab_invalid_encode(self):
        new_file = open(self.testfilepath, "w")
        new_file.write("some text")
        new_file.close()
        
        self.assertRaises(LookupError, self.document_manager.open_tab, self.testfilepath, "invalid_encoding")
        
    def test_tab_label_blank_tab(self):
        self.document_manager.open_tab()
        
        current_page = self.document_manager.get_current_page()
        document = self.document_manager.get_nth_page(current_page)
        
        label_widget = self.document_manager.get_tab_label(document)
        label_text = label_widget.get_children()[0].get_text()
        
        self.assertEquals(constants.MESSAGE_0001, label_text)
        
    def test_tab_label_file_tab(self):
        new_file = open(self.testfilepath, "w")
        new_file.close()
        self.document_manager.open_tab(self.testfilepath)
        
        current_page = self.document_manager.get_current_page()
        document = self.document_manager.get_nth_page(current_page)
        
        label_widget = self.document_manager.get_tab_label(document)
        label_text = label_widget.get_children()[0].get_text()
        
        self.assertEquals(self.testfilename, label_text)
        
    def test_save_active_tab_file_exists(self):
        new_file = open(self.testfilepath, "w")
        new_file.close()
        self.document_manager.open_tab(self.testfilepath)
        
        filebuffer = self.document_manager.get_active_view().buffer
        text = "some text to test"
        filebuffer.set_text(text)
        self.document_manager.save_active_tab()
        
        open_file = open(self.testfilename, "r")
        open_file_text = open_file.read()
        open_file.close()
        
        self.assertEquals(text, open_file_text)
        
    def test_save_tab_file_exists(self):
        new_file = open(self.testfilepath, "w")
        new_file.close()
        self.document_manager.open_tab(self.testfilepath)
        
        document = self.document_manager.get_active_document()
        filebuffer = self.document_manager.get_active_view().buffer
        text = "other text to test"
        filebuffer.set_text(text)
        
        #open another tab to change the active tab
        self.document_manager.open_tab()
        
        self.document_manager.save_tab(document)
        
        open_file = open(self.testfilename, "r")
        open_file_text = open_file.read()
        open_file.close()
        
        self.assertEquals(text, open_file_text)
        
    def test_close_inexistent_tab(self):
        text_buffer = gtksourceview2.Buffer()
        doc = Document(text_buffer)
        
        current_len = len(self.document_manager)
        
        self.assertRaises(ValueError, self.document_manager.close_tab, doc)
        
    def test_close_tab_none_argument(self):
        self.assertRaises(TypeError, self.document_manager.close_tab, None)
        
    def test_close_tab_wrong_argument_type(self):
        self.assertRaises(TypeError, self.document_manager.close_tab, "wrong type argument")

    
    def test_store_tabs_no_documents(self):
        self.document_manager.store_tabs()
        
        store_file_uri = os.path.join(constants.HOME, ".textflow", "stored_tabs")
        store_file = open(store_file_uri, "r")
        text = store_file.read()
        
        self.assertEquals("", text)
    
    