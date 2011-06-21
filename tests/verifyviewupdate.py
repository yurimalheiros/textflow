import unittest

import tf.app

class VerifyViewUpdate(unittest.TestCase):
    def setUp(self):
        tf.app.start(tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        self.toolbutton_undo = self.main_window.toolbutton_undo
        self.toolbutton_redo = self.main_window.toolbutton_redo
        self.document_manager.open_tab()
    
    def test_start_condition(self):
        self.assertFalse(self.toolbutton_undo.get_property("sensitive"))
        self.assertFalse(self.toolbutton_redo.get_property("sensitive"))
    
    def test_toolbar_undo_status(self):
        view = self.document_manager.get_active_view()
        textbuffer = view.buffer
        
        textbuffer.begin_user_action()
        textbuffer.set_text("foo bar test")
        textbuffer.end_user_action()
        
        self.assertTrue(self.toolbutton_undo.get_property("sensitive"))
        self.document_manager.undo()
        self.assertFalse(self.toolbutton_undo.get_property("sensitive"))
        
        self.document_manager.redo()
        
        self.assertTrue(self.toolbutton_undo.get_property("sensitive"))
        
    def test_toolbar_redo_status(self):
        view = self.document_manager.get_active_view()
        textbuffer = view.buffer

        textbuffer.begin_user_action()
        textbuffer.set_text("foo bar test")
        textbuffer.end_user_action()
        
        self.assertFalse(self.toolbutton_redo.get_property("sensitive"))
        self.document_manager.undo()
        self.assertTrue(self.toolbutton_redo.get_property("sensitive"))
        self.document_manager.redo()
        self.assertFalse(self.toolbutton_redo.get_property("sensitive"))
        
    def test_undo_write(self):
        view = self.document_manager.get_active_view()
        textbuffer = view.buffer
        
        textbuffer.begin_user_action()
        textbuffer.set_text("foo bar test")
        textbuffer.end_user_action()
        
        self.document_manager.undo()
        
        textbuffer.begin_user_action()
        textbuffer.set_text("foo bar test 2")
        textbuffer.end_user_action()
        
        self.assertFalse(self.toolbutton_redo.get_property("sensitive"))
        self.assertTrue(self.toolbutton_undo.get_property("sensitive"))
            