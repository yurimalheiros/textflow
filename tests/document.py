import unittest
import os

import tf.app

class Document(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        self.document_manager.open_tab()
        
        current_page_num = self.document_manager.get_current_page()
        self.document = self.document_manager.get_nth_page(current_page_num)
    
    def test_get_current_document(self):
        current_document = self.document_manager.get_active_document()
        self.assertEquals(self.document, current_document)
    
    def test_get_current_view(self):
        current_view = self.document_manager.get_active_view()
        view = self.document.get_children()[0].get_child()
        self.assertEquals(view, current_view)

    def test_notify(self):
        text = "notification test"
        self.document.notify(text)
        notifier = self.document._Document__notifier
        
        self.assertEquals(text, notifier.label)
        self.assertTrue(notifier.get_property("visible"))
        
    def test_open_blank_document(self):
        self.assertEquals("", self.document.file_uri)
        
    def test_open_file_document(self):
        testfile_path = os.path.join(os.getcwd(), "testfile")
        document_file = open(testfile_path, "w")
        self.document_manager.open_tab(testfile_path)
        
        current_page_num = self.document_manager.get_current_page()
        document = self.document_manager.get_nth_page(current_page_num)
        
        self.assertEquals(testfile_path, document.file_uri)
        
        