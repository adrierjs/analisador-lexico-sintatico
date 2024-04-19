class Buffer:
    def __init__(self, program_path):
        self.program_file = open(program_path, 'r')
        self.current_char = self.program_file.read(1)

    def read_next_char(self):
        char = self.current_char
        self.current_char = self.program_file.read(1)
        return char if char else ''

    def pushback(self, char):
        if char:
            self.program_file.seek(self.program_file.tell() - 1)

    def close(self):
        self.program_file.close()
