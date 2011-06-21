import unittest

import tf.app
from tf.core import constants

class LineCommandRun(unittest.TestCase):
    def setUp(self):
        tf.app.start(argv=(constants.HOME,), tests=True)
        self.main_window = tf.app.main_window
        self.document_manager = self.main_window.document_manager
        self.preferences_manager = self.main_window.preferences_manager
    
    def test_no_tabs_open(self):
        document = self.document_manager.get_active_document()
        
        self.assertEquals(1, len(self.document_manager))
        self.assertEquals("", document.get_text())
        self.assertEquals("", document.file_uri)
        
    def test_filebrowser_dir(self):
        filebrowser_dir = self.preferences_manager.get_value("filebrowser_dir")
        self.assertEquals(constants.HOME, filebrowser_dir)
        
    def test_last_dir(self):
        last_dir = self.main_window.last_dir
        self.assertEquals(constants.HOME, last_dir)