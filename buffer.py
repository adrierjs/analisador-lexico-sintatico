class Buffer:
    def __init__(self, program_path):
        #abre o arquivo em modo de leitura
        self.program_file = open(program_path, 'r')
        #inicia com o primeiro caractere do arquivo
        self.current_char = self.program_file.read(1)

    #lê o próximo caractere do arquivo e o retorna. 
    #atualiza o atributo current_char. Se o arquivo estiver vazio, retorna uma string vazia.
    def read_next_char(self):
        char = self.current_char
        self.current_char = self.program_file.read(1)
        return char if char else ''

    #Se houver um caractere válido para devolver, ele utiliza a função seek do objeto de arquivo para mover o ponteiro de leitura de volta em uma posição. 
    #Isso é feito subtraindo 1 do resultado de tell(), que retorna a posição atual do ponteiro de leitura.
    def pushback(self, char):
        if char:
            self.program_file.seek(self.program_file.tell() - 1)

    def close(self):
        self.program_file.close()
