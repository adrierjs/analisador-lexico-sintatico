from tokens import TokenType

class InfixParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.buffer = []  # Buffer para armazenar os tokens
        self.confirm_token()  # Preenche o buffer inicialmente

    def confirm_token(self):
        if self.buffer:
            self.buffer.pop(0)

        while len(self.buffer) < 10:  # BUFFER_SIZE
            next_token = self.lexer.read_next_token()

            if next_token.token_type == TokenType.COMMENT:
                continue

            self.buffer.append(next_token)

            if next_token.token_type == TokenType.EOF:
                break

    def print_match_token(self, token):
        print("Match " + str(token))
        if token.token_type == TokenType.PONTO_VIRGULA:
            print("")

    def lookahead(self, k):
        if len(self.buffer) >= k:
            return self.buffer[k-1]
        else:
            return None
        
    def match(self, token_type):
        la = self.lookahead(1)

        if la.token_type == token_type:
            self.print_match_token(la)
            try:
                self.confirm_token()
            except RuntimeError as ex:
                print(ex)
        else:
            raise SyntaxError(f"Expected {token_type}, found {la.token_type}")

    def parse(self):
        try:
            self.calculadora()
        except SyntaxError as e:
            print("Erro de sintaxe:", e)
            print("Expressão não pôde ser analisada corretamente.")
        finally:
            self.close()

    # Regra: calculadora: calculo_list EOF;
    def calculadora(self):
        self.calculo_list()
        self.match(TokenType.EOF)

    # Regra: calculo_list: calculo*;
    def calculo_list(self):
        token = self.lookahead(1)
        while token.token_type in [TokenType.ABRE_PAR, TokenType.CONST_INT, TokenType.CONST_FLOAT, TokenType.OP_SUB, TokenType.OP_SUM]:
            self.calculo()
            token = self.lookahead(1)

    # Regra: calculo: expr_arit ';';
    def calculo(self):
        self.expr_arit()
        self.match(TokenType.PONTO_VIRGULA)
        
    # Regra: expr_arit: termo expr_arit_sub_regra;
    def expr_arit(self):
        self.termo()
        self.expr_arit_sub_regra()

    # Regra: expr_arit_sub_regra: (('+' | '-') expr_arit)*;
    def expr_arit_sub_regra(self):
        token = self.lookahead(1)

        if token.token_type in [TokenType.OP_SUM, TokenType.OP_SUB]:
            self.match(token.token_type)
            self.expr_arit()
    
    # Regra: termo: fator termo_sub_regra;
    def termo(self):
        self.fator()
        self.termo_sub_regra()

    # Regra: termo_sub_regra: (('*' | '/') termo);
    def termo_sub_regra(self):
        token = self.lookahead(1)

        if token.token_type in [TokenType.OP_MUL, TokenType.OP_DIV]:
            self.match(token.token_type)
            self.termo()

    # Regra: fator: sinal? (CONST_INT | CONST_FLOAT | '(' expr_arit ')');
    def fator(self):
        self.sinal()

        token = self.lookahead(1)

        if token.token_type in [TokenType.CONST_INT, TokenType.CONST_FLOAT]:
            self.match(token.token_type)
        elif token.token_type == TokenType.ABRE_PAR:
            self.match(TokenType.ABRE_PAR)
            self.expr_arit()
            self.match(TokenType.FECHA_PAR)
        else:
            raise SyntaxError("Unexpected token: " + str(token))

    # Regra: sinal: '+' | '-';
    def sinal(self):
        token = self.lookahead(1)

        if token.token_type in [TokenType.OP_SUM, TokenType.OP_SUB]:
            self.match(token.token_type)

    def close(self):
        self.lexer.close()
