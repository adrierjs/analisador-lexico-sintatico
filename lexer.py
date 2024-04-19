from buffer import Buffer
from tokens import Token, TokenType

class Lexer:
    def __init__(self, program_path):
        # Inicialização do buffer com o caminho do programa
        self.buffer = Buffer(program_path)

        # Dicionários para mapear operadores e caracteres especiais para os tipos de token correspondentes
        self.operators = {'+': TokenType.OP_SUM, '-': TokenType.OP_SUB, '*': TokenType.OP_MUL, '/': TokenType.OP_DIV}
        self.char_special = {'(': TokenType.ABRE_PAR, ')': TokenType.FECHA_PAR, ';': TokenType.PONTO_VIRGULA}

        # Variável para armazenar o último caractere lido
        self.last_char = None

    def read_next_token(self):
        while True:
            # Usa o último caractere lido se estiver disponível, caso contrário, lê do buffer
            char = self.last_char if self.last_char is not None else self.buffer.read_next_char()
            # Reseta a variável last_char
            self.last_char = None

            # Verifica se o caractere atual é o fim do arquivo
            if char == '':
                return Token(TokenType.EOF, None)
            # Ignora caracteres de espaço em branco
            elif char.isspace():
                continue
            # Verifica se o caractere atual é um operador
            elif char in self.operators:
                return self.read_operator(char)
            # Verifica se o caractere atual é um caractere especial
            elif char in self.char_special:
                return self.read_char_special(char)
            # Verifica se o caractere atual é um dígito
            elif char.isdigit():
                return self.read_number(char)
            else:
                raise RuntimeError("Lexema não reconhecido")

    def read_operator(self, initial_symbol):
        # Verifica se o operador é um sinal de subtração, caso contrário, retorna o tipo de token correspondente
        #tratou primeiro o '-' pq estava considerando numero negarivo e nao um OP_SUB
        # if initial_symbol == '-':
        #     return Token(TokenType.OP_SUB, initial_symbol)
        # else:
            return Token(self.operators[initial_symbol], initial_symbol)


    def read_char_special(self, initial_symbol):
        # Retorna o tipo de token correspondente para caracteres especiais
        return Token(self.char_special[initial_symbol], initial_symbol)

    def read_number(self, initial_symbol):
        # Inicializa o lexema com o dígito inicial
        lexeme = initial_symbol
        # Variável para indicar se o número tem ponto decimal
        has_decimal_point = False
        # Variável para indicar se o último caractere foi um dígito
        last_was_digit = initial_symbol.isdigit()
        
        while True:
            # Lê o próximo caractere do buffer
            char = self.buffer.read_next_char()
            
            # Se o caractere for um dígito, adiciona ao lexema e atualiza last_was_digit
            if char.isdigit():
                lexeme += char
                last_was_digit = True
            # Se ainda não tiver ponto decimal e o caractere for um '.', adiciona ao lexema e atualiza has_decimal_point e last_was_digit
            elif not has_decimal_point and char == '.':
                lexeme += char
                has_decimal_point = True
                last_was_digit = False
            # Se o último caractere não foi um dígito e o caractere atual for um '-', coloca o caractere de volta no buffer e sai do loop
            elif not last_was_digit and char == '-':
                self.buffer.pushback(char)
                break
            # Se não for um dígito, ponto decimal ou sinal de menos, coloca o caractere de volta no buffer e sai do loop
            else:
                self.last_char = char
                break

        # Se o último caractere não foi um dígito, lança um erro
        if not last_was_digit:
            raise RuntimeError("Lexema não reconhecido")
        
        # Retorna o token correspondente ao número (inteiro ou float) com seu lexema
        return Token(TokenType.CONST_FLOAT if has_decimal_point else TokenType.CONST_INT, lexeme)

    def close(self):
        self.buffer.close()
