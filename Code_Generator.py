class CodeGenerator:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.temp_begin = 1000
        self.temp_offset = 0

    def get_temp(self):
        x = self.temp_offset
        self.temp_offset += 4
        return self.temp_begin + x

    def code_gen(self, func, LA):
        if func == "assignAddr":
            self.symbol_table.add_adress(LA)
        elif func == "pid":
            pass
        elif func == "increaseAddr":
            pass
        elif func == "newScope":
            pass
        elif func == "setType":
            pass
        elif func == "increaseAddr":
            pass
        elif func == "save":
            pass
        elif func == "justSave":
            pass
        elif func == "setConditional":
            pass
        elif func == "setUnconditional":
            pass
        elif func == "setJump":
            pass
        elif func == "setConditionalFor":
            pass
        elif func == "compare":
            pass
        elif func == "add":
            pass
        elif func == "mult":
            pass
        elif func == "negate":
            pass
        elif func == "pushNum":
            pass
        elif func == "print":
            pass