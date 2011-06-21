import unittest

from tf.com.snippetsparser import Lex

class LexTest(unittest.TestCase):
    def setUp(self):
        self.parser = Lex()
    
    def test_get_next_char(self):
        self.parser.text = "foo bar"
        
        char = self.parser._Lex__get_next_char()
        self.assertEquals(char, "f")
        
        char = self.parser._Lex__get_next_char()
        self.assertEquals(char, "o")
        
        for i in range(5):
            char = self.parser._Lex__get_next_char()
        
        self.assertEquals(char, "r")
            
    def test_get_number(self):
        self.parser.text = "12345"
        self.parser._Lex__get_next_char()
        
        simbol = self.parser._Lex__get_number()
        self.assertEquals(simbol, "12345")
        
        self.parser.text = "12345x"
        self.parser.pos = 0
        self.parser._Lex__get_next_char()
        
        simbol = self.parser._Lex__get_number()
        self.assertEquals(simbol, "12345")
    
    def test_get_text(self):
        self.parser.text = "foo bar"
        self.parser._Lex__get_next_char()
        
        simbol = self.parser._Lex__get_text()
        self.assertEquals(simbol, "foo bar")
        
        self.parser.text = "foo bar 1"
        self.parser.pos = 0
        self.parser._Lex__get_next_char()
        
        simbol = self.parser._Lex__get_text()
        self.assertEquals(simbol, "foo bar ")
    
    def test_empty(self):
        text = ""
        empty_list = []

        simbols = self.parser.run(text)
        
        self.assertEquals(simbols, empty_list)
        
    def test_simbols(self):
        text = "text 123$ more text{and more} 032: 8%foo/bar/lol\\escape"
        result_list = [(0, "text "),
                       (1, "123"),
                       (2, "$"),
                       (0, " more text"),
                       (3, "{"),
                       (0, "and more"),
                       (4, "}"),
                       (0, " "),
                       (1, "032"),
                       (5, ":"),
                       (0, " "),
                       (1, "8"),
                       (6, "%"),
                       (0, "foo"),
                       (7, "/"),
                       (0, "bar"),
                       (7, "/"),
                       (0, "lol"),
                       (8, "\\"),
                       (0, "escape")]

        simbols = self.parser.run(text)
        
        self.assertEquals(simbols, result_list)
