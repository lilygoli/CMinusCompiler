# authors: Mohammad Saneian 96109769 Leili Goli 96106044

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

    def add_addr(self, LA):
        for i in range(len(self.symbol_table) - 1, -1, -1):
            if self.symbol_table[i].lexeme == LA:
                self.symbol_table[i].address = self.begin_addr + self.offset
                self.offset += 4
                self.symbol_table[i].type = self.cur_type
                if self.new_scope:
                    self.scope_stack.push(len(self.symbol_table) - 1)
                    self.new_scope = False
            break
        # print("XXX", self.symbol_table[i].address, LA, self.scope_stack.stack)

    def set_type(self, LA):
        self.cur_type = LA

    def find_addr(self, LA):
        end = len(self.symbol_table)
        for i in range(self.scope_stack.get_len() - 1, -1, -1):
            for j in range(self.scope_stack.get_element(i), end):
                if self.symbol_table[j].lexeme == LA:
                    return self.symbol_table[j].address
            end = self.scope_stack.get_element(i)

        return None

    def end_scope(self):  # should be called after function finishes
        self.scope_stack.pop(1)
