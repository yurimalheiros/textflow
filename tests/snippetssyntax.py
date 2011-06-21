import unittest

from tf.ui.mainwindow import MainWindow
from tf.com.snippetsparser import Syntax

class SyntaxTest(unittest.TestCase):
    def setUp(self):
        self.main_window = MainWindow(tests=True)
        self.document_manager = self.main_window.document_manager
        self.document_manager.open_tab()
        
        self.view = self.document_manager.get_active_view()
        self.document = self.document_manager.get_active_document()
        self.syntax = Syntax(self.view, [])
    
    def test_get_next_token(self):
        self.syntax.tokens = [(0, "foo"), (1, "123")]
        
        token = self.syntax._Syntax__get_next_token()
        self.assertEquals(token, (0, "foo"))
        
        token = self.syntax._Syntax__get_next_token()
        self.assertEquals(token, (1, "123"))
    
    def test_empty(self):
        
        self.syntax.tokens = []
        self.syntax.parse()

        text = self.document.get_text()
        self.assertEquals(text, "")
    
    def test_number_and_text(self):
        
        self.syntax.tokens = [(0, "foo"), (1, "123")]
        self.syntax.parse()

        text = self.document.get_text()
        self.assertEquals(text, "foo123")
            