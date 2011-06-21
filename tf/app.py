from tf.mainwindow import MainWindow
from tf.documentmanager import DocumentManager
from tf.preferences import Preferences
from tf.core.languagemanager import LanguageManager
from tf.core.triggermanager import TriggerManager
from tf.core import constants

main_window = None
document_manager = None
preferences_manager = None
language_manager = None
trigger_manager = None

def start(argv=None, tests=False):
    global preferences_manager
    global document_manager
    global main_window
    global language_manager
    global trigger_manager
    
    preferences_manager = Preferences()
    trigger_manager = TriggerManager()
    language_manager = LanguageManager()
    document_manager = DocumentManager()
    main_window = MainWindow(argv, tests)
    main_window.run(argv, tests)
    