from tokens import Token, TokenType
from lexer import Lexer
from parser_infixa import InfixParser
from parser_prefixa import PrefixParser

def main():
    # PARSER INFIXA
    # lexer = Lexer("expressoes_infixas.txt")
    # parser = InfixParser(lexer)
    # parser.parse()

    # PARSER PREFIXA
    lexer = Lexer("expressoes_prefixa.txt")
    parser = PrefixParser(lexer)
    parser.parse()

if __name__ == "__main__":
    main()