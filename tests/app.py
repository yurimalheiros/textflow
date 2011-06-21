import unittest
import gtk
import time

import tf.app
from tf.mainwindow import MainWindow
from tf.documentmanager import DocumentManager
from tf.preferences import Preferences
from tf.core import constants

class App(unittest.TestCase):
    def test_start_app(self):
        tf.app.start(tests=True)
        self.assertTrue(isinstance(tf.app.main_window, MainWindow))
        self.assertTrue(isinstance(tf.app.document_manager, DocumentManager))
        self.assertTrue(isinstance(tf.app.preferences_manager, Preferences))
        self.assertTrue(tf.app.constants == constants)
        