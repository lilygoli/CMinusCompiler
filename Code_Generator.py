class CodeGenerator:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.temp_begin = 1000
        self.temp_offset = 0

    def get_temp(self):
        x = self.temp_offset
        self.temp_offset += 4
        return self.temp_begin + x
