import unittest

from tests.app import App
from tests.documentmanager import DocumentManager
from tests.document import Document
from tests.verifyviewupdate import VerifyViewUpdate
from tests.linecommandrun import LineCommandRun
from tests.externalfilemodification import ExternalFileModification
from tests.openlinetrigger import OpenLineTrigger
from tests.openlineabovetrigger import OpenLineAboveTrigger
#from tests.snippetslex import LexTest
#from tests.snippetssyntax import SyntaxTest

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DocumentManager))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Document))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(VerifyViewUpdate))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LineCommandRun))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ExternalFileModification))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(OpenLineTrigger))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(OpenLineAboveTrigger))
#suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LexTest))
#suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SyntaxTest))

unittest.TextTestRunner(verbosity=2).run(suite)