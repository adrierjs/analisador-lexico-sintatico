from buffer import Buffer
from tokens import Token, TokenType

class Lexer:
    def __init__(self, program_path):
        self.buffer = Buffer(program_path)

        self.operators = {'+': TokenType.OP_SUM, '-': TokenType.OP_SUB, '*': TokenType.OP_MUL, '/': TokenType.OP_DIV}
        self.char_special = {'(': TokenType.ABRE_PAR, ')': TokenType.FECHA_PAR, ';': TokenType.PONTO_VIRGULA}

        self.last_char = None

    def read_next_token(self):
        while True:
            char = self.last_char if self.last_char is not None else self.buffer.read_next_char()
            self.last_char = None

            if char == '':
                return Token(TokenType.EOF, None)
            elif char.isspace():
                continue
            elif char in self.operators:
                return self.read_operator(char)
            elif char in self.char_special:
                return self.read_char_special(char)
            elif char.isdigit():
                return self.read_number(char)
            else:
                raise RuntimeError("Lexema não reconhecido")

    def read_operator(self, initial_symbol):
        return Token(self.operators[initial_symbol], initial_symbol)


    def read_char_special(self, initial_symbol):
        return Token(self.char_special[initial_symbol], initial_symbol)

    def read_number(self, initial_symbol):
        lexeme = initial_symbol
        has_decimal_point = False
        last_was_digit = initial_symbol.isdigit()
        
        while True:
            char = self.buffer.read_next_char()
            
            if char.isdigit():
                lexeme += char
                last_was_digit = True
            elif not has_decimal_point and char == '.':
                lexeme += char
                has_decimal_point = True
                last_was_digit = False
            elif not last_was_digit and char == '-':
                self.buffer.pushback(char)
                break
            else:
                self.last_char = char
                break

        if not last_was_digit:
            raise RuntimeError("Lexema não reconhecido")
        
        return Token(TokenType.CONST_FLOAT if has_decimal_point else TokenType.CONST_INT, lexeme)

    def close(self):
        self.buffer.close()
