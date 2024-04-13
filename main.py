from lexer import Lexer
from tokens import TokenType

def main():
    program_path = 'arquivo.txt' 
    lexer = Lexer(program_path)

    try:
        while True:
            token = lexer.read_next_token()
            print(token)
            if token.token_type == TokenType.EOF:
                break
    finally:
        lexer.close()

if __name__ == "__main__":
    main()
