import unittest

import tf.app
from tf.widgets.document import Document
from tf.triggers.openlineabove import OpenLineAbove

class OpenLineAboveTrigger(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        self.document_manager.open_tab()
        self.openlineabove_trigger = OpenLineAbove()
        
    def test_open_line_above_between_lines(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one\nline two")
        self.openlineabove_trigger.activate()
        
        self.assertEquals("line one\n\nline two", doc.get_text())
        
    def test_open_line_one_line(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one")
        textbuffer.place_cursor(textbuffer.get_start_iter())
        self.openlineabove_trigger.activate()
        
        self.assertEquals("\nline one", doc.get_text())
        
    def test_open_line_one_line_with_indentation(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("\tline one")
        textbuffer.place_cursor(textbuffer.get_start_iter())
        self.openlineabove_trigger.activate()
        
        self.assertEquals("\t\n\tline one", doc.get_text())
        
    def test_open_line_one_line_cursor_at_start(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        textbuffer.insert_at_cursor("line one")
        
        textiter = textbuffer.get_start_iter()
        
        textbuffer.place_cursor(textiter)
        self.openlineabove_trigger.activate()
        
        self.assertEquals("\nline one", doc.get_text())
        
    def test_open_line_no_lines(self):
        doc = self.document_manager.get_active_document()
        textbuffer = doc.buffer
        self.openlineabove_trigger.activate()
        
        self.assertEquals("\n", doc.get_text())
        
    