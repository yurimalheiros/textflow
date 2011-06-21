from strongwind import *
from textflow import *

from tf.core import constants

app = launchTextFlow("./textflow")
frame = app.textflowFrame


def test_ctrl_d():
    textview = frame.findText(None)
    textview.enterText("some text to test")
    textview.keyCombo("<ctrl>d")
    app.textflowFrame.assertResult("", textview.text)
    
def test_open_invalid_path():
    #show open dialog
    toolbutton_open = frame.findPushButton(constants.MESSAGE_0003)
    toolbutton_open.mouseClick()
    
    #enter text on open dialog
    open_dialog = app.findDialog(constants.MESSAGE_0003)
    text_input = open_dialog.findText(None)
    text_input.enterText("/invalid/path")
    
    #click on open button
    open_button = open_dialog.findPushButton(constants.MESSAGE_0003)
    open_button.mouseClick()
    
    #assert
    error_alert = app.findAlert(None)
    frame.assertResult(True, error_alert != None)

    error_alert = error_alert.findPushButton(None)
    error_alert.mouseClick()
    
#Running tests

#test_ctrl_d()
test_open_invalid_path()
