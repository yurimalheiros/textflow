# -*- coding: utf-8 -*-

"""
Application wrapper for TextFlow
"""

from strongwind import *
import os

from tf.core import constants

def launchTextFlow(exe=None):
    """
    Launch TextFlow with accessibility enabled.
    """
    
    if exe is None:
        exe = "/usr/bin/textflow"
        
    args = [exe]
    (app, subproc) = cache.launchApplication(args=args)
    
    textflow = TextFlow(app, subproc)
    cache.addApplication(textflow)
    
    textflow.textflowFrame.app = textflow
    
    return textflow
    
class TextFlow(accessibles.Application):
    def __init__(self, accessible, subproc=None):
        super(TextFlow, self).__init__(accessible, subproc)
        self.findFrame(constants.MESSAGE_0001, logName="TextFlow")
