import unittest

import tf.app
from tf.widgets.document import Document
from tf.triggers.openline import OpenLine

class OpenLineTrigger(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        self.document_manager.open_tab()
        self.openline_trigger = OpenLine()
        
    def test_open_line_between_lines(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one\nline two")
        textbuffer.place_cursor(textbuffer.get_start_iter())
        self.openline_trigger.activate()
        
        self.assertEquals("line one\n\nline two", doc.get_text())
        
    def test_open_line_one_line(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one")
        textbuffer.place_cursor(textbuffer.get_start_iter())
        self.openline_trigger.activate()
        
        self.assertEquals("line one\n", doc.get_text())
        
    def test_open_line_one_line_with_indentation(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("\tline one")
        textbuffer.place_cursor(textbuffer.get_start_iter())
        self.openline_trigger.activate()
        
        self.assertEquals("\tline one\n\t", doc.get_text())
        
    def test_open_line_one_line_cursor_at_end(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one")
        
        textiter = textbuffer.get_start_iter()
        textiter.forward_to_line_end()
        
        textbuffer.place_cursor(textiter)
        self.openline_trigger.activate()
        
        self.assertEquals("line one\n", doc.get_text())
        
    def test_open_line_no_lines(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        self.openline_trigger.activate()
        
        self.assertEquals("\n", doc.get_text())
        
    