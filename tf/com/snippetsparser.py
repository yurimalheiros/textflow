import re

class Lex(object):
    """
    This class is the TextFlow snippets lexical analyser.
    """
    def __init__(self):
        """
        Constructor.
        """
        
        self.text = None
        self.pos = 0
    
    def run(self, text):
        """
        Execute the parser for a text.
        
        @param text: The text that will be parsed.
        @type text: A string.
        """
        self.text = text
        self.pos = 0
        simbol_list = []
        
        num_regex = "[0-9]"
        
        while self.pos < len(self.text):
            char = self.__get_next_char()
            
            if re.match(num_regex, char):
                number = self.__get_number()
                simbol = (1, number)
            elif char == "$":
                simbol = (2, "$")
            elif char == "{":
                simbol = (3, "{")
            elif char == "}":
                simbol = (4, "}")
            elif char == ":":
                simbol = (5, ":")
            elif char == "%":
                simbol = (6, "%")
            elif char == "/":
                simbol = (7, "/")
            elif char == "\\":
                simbol = (8, "\\")
            else:
                text = self.__get_text()
                simbol = (0, text)
        
            simbol_list.append(simbol)
            
        return simbol_list
    
    def __get_next_char(self):
        """
        Returns the next char.
        """
        char = self.text[self.pos]
        self.pos += 1
        
        return char
        
    def __get_number(self):
        """
        Returns a number starting in last get char.
        """
        number_list = [self.text[self.pos - 1]]
        
        while self.pos < len(self.text):
            char = self.__get_next_char()
            
            if re.match("[0-9]", char):
                number_list.append(char)
            else:
                self.pos -= 1
                break
                
        number = ''.join(number_list)
        return number
        
    def __get_text(self):
        """
        Returns a text starting in last get char.
        """
        text_list = [self.text[self.pos - 1]]
        regex = "[0-9${}:%/\\\\]" 
        
        while self.pos < len(self.text):
            char = self.__get_next_char()
            
            if re.match(regex, char):
                self.pos -= 1
                break
            else:
                text_list.append(char)
                
        text = ''.join(text_list)
        return text

class Syntax(object):
    """
    This class is the TextFlow snippets syntactical analyser.
    """
    
    def __init__(self, view, tokens):
        """
        Constructor.
        """
        self.view = view
        self.buffer = view.buffer
        self.tokens = []
        self.pos = 0 
    
    def __get_next_token(self):
        """
        Return the next token.
        """
        token = self.tokens[self.pos]
        self.pos += 1
        
        return token
        
    def parse(self):
        """
        Run the syntactical analyser.
        """
        
        while self.pos < len(self.tokens):
            token = self.__get_next_token()
            
            if token[0] == 0:
                self.buffer.insert_at_cursor(token[1])
            elif token[0] == 1:
                self.buffer.insert_at_cursor(token[1])
            
            self.parse()