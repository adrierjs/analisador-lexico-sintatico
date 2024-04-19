from tokens import Token, TokenType
from lexer import Lexer
from parser_infixa import InfixParser
from parser_prefixa import PrefixParser

def main():
    #LEXER
    input_file_path = "expressoes_prefixa.txt"    
    lexer = Lexer(input_file_path)
    try:
        # Lendo os tokens do programa e imprimindo-os
        while True:
            token = lexer.read_next_token()
            print(token)
            if token.token_type == TokenType.EOF:
                break
    except RuntimeError as e:
        print("Erro durante a análise léxica:", e)
    lexer.close()
    
    # PARSER INFIXA
    lexer = Lexer("expressoes_infixas.txt")
    parser = InfixParser(lexer)
    parser.parse()

    # PARSER PREFIXA
    lexer = Lexer("expressoes_prefixa.txt")
    parser = PrefixParser(lexer)
    parser.parse()

if __name__ == "__main__":
    main()