import gobject
import gio

import tf.app
from tf.core import constants

class ModificationMonitor(gobject.GObject):
    
    __gsignals__ = { "change" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                                 (gobject.TYPE_STRING,)) }
                                 
    def __init__(self, document_manager):
        """
        Constructor.
        """
        super(ModificationMonitor, self).__init__()
        self.document_manager = tf.app.document_manager
        self.monitors = {}
        
        self.document_manager = document_manager
        self.document_manager.connect("save-file", self.file_save)
        self.document_manager.connect("open-file", self.file_open)
        self.document_manager.connect("close-file", self.file_close)
        
    def add(self, document):
        """
        Monitor the changes of a document
        
        @param document: A document.
        @type document: A Document object.
        """
        mfile = gio.File(document.file_uri)
        monitor = mfile.monitor_file()
        cb_id = monitor.connect("changed", self.changec, document)
        self.monitors[document] = (mfile, monitor, cb_id)
        
        
    def remove(self, document):
        """
        Remove from monitoring a document
        
        @param document: A document.
        @type document: A Document object.
        """
        mfile, monitor, cb_id = self.monitors[document]
        monitor.disconnect(cb_id)
        monitor.cancel()
        
        self.monitors.pop(document)
        
    def changec(self, monitor, f1, f2, event, document):
        print "mudou"
        if f1.query_exists():
            file_text = f1.read().read()
            file_text = unicode(file_text, document.encode)            
            file_text = file_text.replace("\r","").replace('\0', '')
            
            if event == gio.FILE_MONITOR_EVENT_CHANGES_DONE_HINT:
                if document.get_text() != file_text:
                    document.notify(constants.MESSAGE_0032 % document.file_uri)
                    return True
        
        return False
        
    def file_save(self, document_manager, document):
        if document in self.monitors.keys():
            if document.file_uri != self.monitors[document][0].get_path():
                self.remove(document)
                self.add(document)
        else:
            self.add(document)
                
    def file_open(self, document_manager, document):
        if document.file_uri != "":
            self.add(document)
                    
    def file_close(self, document_manager, document):
        if document.file_uri != "":
            self.remove(document)
