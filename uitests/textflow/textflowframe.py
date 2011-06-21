from strongwind import *
from textflow import *

class TextflowFrame(accessibles.Frame):
    logName = "TextFlow"
    
    def __init__(self, accessible):
        super(TextflowFrame, self).__init__(accessible)

    def assertResult(self, expected, value):
        procedurelogger.expectedResult('Value obtained: %s. - Expected result: %s.' % (value, expected))
 	
     	def resultMatches():
         	return expected == value
     	
     	assert retryUntilTrue(resultMatches) 
