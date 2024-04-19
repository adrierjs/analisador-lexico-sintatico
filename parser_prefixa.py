from tokens import TokenType

class PrefixParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.buffer = []
        self.confirm_token()

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
            self.calculo_list() 
        except SyntaxError as e:
            print("Erro de sintaxe:", e)
            print("Expressão não pôde ser analisada corretamente.")
        finally:
            self.close() 

    # Regra calculo_list: calculo*
    def calculo_list(self):
        token = self.lookahead(1)
        firsts = [
            TokenType.OP_SUM,
            TokenType.OP_SUB,
            TokenType.OP_MUL,
            TokenType.OP_DIV,
            TokenType.CONST_INT,
            TokenType.CONST_FLOAT
        ]

        if token.token_type in firsts:
            self.calculo()  
            self.calculo_list() 

    # Regra calculo: expr_arit ';'
    def calculo(self):
        self.expr_arit()
        self.match(TokenType.PONTO_VIRGULA)

    # Regra expr_arit: operador expr_arit_sub_regra | operando
    def expr_arit(self):
        token = self.lookahead(1)

        if token.token_type in [
            TokenType.OP_SUM,
            TokenType.OP_SUB,
            TokenType.OP_MUL,
            TokenType.OP_DIV
        ]:
            self.match(token.token_type)
            self.expr_arit_sub_regra()  
        elif token.token_type in [TokenType.CONST_INT, TokenType.CONST_FLOAT]:
            self.operando()
        else:
            raise SyntaxError(f"Unexpected token {token.token_type}")

    # Regra expr_arit_sub_regra: operando expr_arit_sub_regra | ε
    def expr_arit_sub_regra(self):
        token = self.lookahead(1)

        if token.token_type == TokenType.PONTO_VIRGULA:
            return
        else:
            self.expr_arit()
            self.expr_arit_sub_regra()

    # Regra 'operando: CONST_INT | CONST_FLOAT'.
    def operando(self):
        token = self.lookahead(1)

        if token.token_type in [TokenType.CONST_INT, TokenType.CONST_FLOAT]:
            self.match(token.token_type)
        else:
            raise SyntaxError(f"Esperando {token.token_type}")

    

    def close(self):
        self.lexer.close()