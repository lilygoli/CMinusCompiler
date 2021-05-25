from Stack import Stack


class SymbolTable:

    def __init__(self):
        self.symbol_table = []
        self.new_scope = True
        self.scope_stack = Stack()
        self.cur_type = 'int'
        self.begin_addr = 500
        self.offset = 0

    class Record:
        def __init__(self, lexeme):
            self.lexeme = lexeme
            self.type = None
            self.address = None

    def add_symbol(self, lexeme):
        record = self.Record(lexeme)
        self.symbol_table.append(record)

    def add_address(self, LA):
        for i in range(len(self.symbol_table) - 1, 0):
            if self.symbol_table[i].lexeme == LA:
                self.symbol_table[i].address = self.begin_addr + self.offset
                self.offset += 4
                self.symbol_table[i].type = self.cur_type
                if self.new_scope:
                    self.scope_stack.push(len(self.symbol_table) - 1)
                    self.new_scope = False
            break

    def set_type(self, LA):
        self.cur_type = LA

    def get_addr(self, LA):
        end = len(self.symbol_table)
        for i in range(self.scope_stack.get_len() - 1, 0):
            for j in range(self.scope_stack.get_element(i), end - 1):
                if self.symbol_table[j].lexeme == LA:
                    return self.symbol_table[j].addrress
            end = self.scope_stack.get_element(i)
        return None

    def end_scope(self):  # should be called in Return statements
        self.symbol_table.pop(1)
