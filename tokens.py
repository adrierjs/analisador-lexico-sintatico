from enum import Enum

class TokenType(Enum):
    CONST_INT = 1
    CONST_FLOAT = 2
    OP_SUM = 3
    OP_SUB = 4
    OP_MUL = 5
    OP_DIV = 6
    ABRE_PAR = 7
    FECHA_PAR = 8
    PONTO_VIRGULA = 9
    EOF = 10
    COMMENT = 11

class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __str__(self):
        return f"Token({self.token_type.name}, {self.lexeme})"
