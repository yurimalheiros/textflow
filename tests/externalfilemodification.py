import gobject
import time
import os
import gtk
import gtksourceview2
import gio

import unittest

import tf.app
from tf.com.modificationmonitor import ModificationMonitor
from tf.widgets.document import Document

class ExternalFileModification(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        
        self.modification_monitor = ModificationMonitor(self.document_manager)
        self.document_manager = self.modification_monitor.document_manager
        
        self.testfilename = "testfile"
        self.testfilepath = os.path.join(os.getcwd(), self.testfilename)
        
        self.testfile = open(self.testfilepath, "w")
        self.testfile.close()
        
        self.gio_file = gio.File(self.testfilepath)
        
        document_buffer = gtksourceview2.Buffer()
        self.test_document = Document(document_buffer, self.testfilepath)
        
    def tearDown(self):
        if os.path.exists(self.testfilepath):
            os.remove(self.testfilepath)

    def test_change_uri_change_file(self):
        self.modification_monitor.add(self.test_document)
        self.document_manager
        self.test_document.file_uri = os.path.join(os.getcwd(), "testfile2")
        
        self.modification_monitor.file_save(self.document_manager,
                                            self.test_document)
                   
        mfile, monitor, cb_id = self.modification_monitor.monitors[self.test_document]
        
        
        self.assertEquals(self.test_document.file_uri, mfile.get_path())

    def test_add_document(self):
        self.modification_monitor.add(self.test_document)
        
        self.assertEquals(1, len(self.modification_monitor.monitors))
        
    def test_add_multiple_documents(self):
        self.modification_monitor.add(self.test_document)
        
        document_buffer = gtksourceview2.Buffer()
        other_document = Document(document_buffer, self.testfilepath)
        
        self.modification_monitor.add(other_document)
        
        self.assertEquals(2, len(self.modification_monitor.monitors))

    def test_remove_document(self):
        self.modification_monitor.add(self.test_document)
        
        document_buffer = gtksourceview2.Buffer()
        other_document = Document(document_buffer, self.testfilepath)
        
        self.modification_monitor.add(other_document)
        self.modification_monitor.remove(other_document)
        
        self.assertEquals(1, len(self.modification_monitor.monitors))
            
    def test_file_write(self):
        self.testfile = open(self.testfilepath, "w")
        self.testfile.write("modify!")
        self.testfile.close()
        
        event = gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT
        result = self.modification_monitor.change(self.modification_monitor, self.gio_file,
                                                  None, event, self.test_document)
        
        self.assertTrue(result)
        
        
    def test_file_delete(self):
        os.remove(self.testfilepath)
        
        event = gio.FILE_MONITOR_EVENT_CHANGED
        result = self.modification_monitor.change(self.modification_monitor, self.gio_file,
                                                  None, event, self.test_document)
                                                  
        self.assertFalse(result)
        
    def test_file_only_open_and_close(self):
        event = gio.FILE_MONITOR_EVENT_CHANGED
        result = self.modification_monitor.change(self.modification_monitor, self.gio_file,
                                                  None, event, self.test_document)
                                                  
        self.assertFalse(result)

    def test_open_document(self):
        document_buffer = gtksourceview2.Buffer()
        document = Document(document_buffer, self.testfilepath)
        self.modification_monitor.file_open(self.document_manager, document)
        
        self.assertEquals(1, len(self.modification_monitor.monitors))
        
    def test_open_blank_document(self):
        document_buffer = gtksourceview2.Buffer()
        document = Document(document_buffer)
        self.modification_monitor.file_open(self.document_manager, document)
        
        self.assertEquals(0, len(self.modification_monitor.monitors))
        
    def test_close_document(self):
        document_buffer = gtksourceview2.Buffer()
        document = Document(document_buffer, self.testfilepath)
        
        self.modification_monitor.file_open(self.document_manager, document)
        self.modification_monitor.file_close(self.document_manager, document)
        
        self.assertEquals(0, len(self.modification_monitor.monitors))
        
    def test_revert(self):
        document_buffer = gtksourceview2.Buffer()
        document = Document(document_buffer, self.testfilepath)
        
        text = "modify!"
        self.testfile = open(self.testfilepath, "w")
        self.testfile.write(text)
        self.testfile.close()
        
        document.revert()
        
        self.assertEquals(text, document.get_text())