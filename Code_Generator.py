from Stack import Stack


class CodeGenerator:

    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.temp_begin = 1000
        self.temp_offset = 0
        self.ss = Stack()
        self.PB = []
        self.i = 0

    def get_temp(self):
        x = self.temp_offset
        self.temp_offset += 4
        return self.temp_begin + x

    def code_gen(self, func, LA):
        if func == "assignAddr":
            self.symbol_table.add_addr(LA)
        elif func == "pid":
            p = self.symbol_table.find_addr(LA)
            self.ss.push(p)
        elif func == "increaseAddr":
            self.symbol_table.offset += (int(LA) - 1) * 4
        elif func == "newScope":
            self.symbol_table.new_scope = True
        elif func == "setType":
            self.symbol_table.set_type(LA)
        elif func == "save":
            self.PB += [None]
            self.ss.push(self.i)
            self.i += 1
        elif func == "justSave":
            self.ss.push(self.i)
        elif func == "setConditional":
            self.PB[self.ss[self.ss.top - 1]] = f"(JPF, {self.ss[self.ss.top - 2]}, {self.i}, )"
            self.i += 1
        elif func == "setUnconditional":
            self.PB[self.ss[self.ss.top - 1]] = f"(JP, {self.i}, ,)"
            self.ss.pop(3)
            self.i += 1
        elif func == "setJump":
            self.PB[self.i] = f"(JP, {self.ss[self.ss.top - 1]}, ,)"
            self.ss.pop(1)
            self.i += 1
        elif func == "setConditionalFor":
            self.PB[self.ss.top] = f"(JPF, {self.ss[self.ss.top - 2]}, {self.i}, )"
            self.ss.pop(3)
            self.i += 1
        elif func == "compare":
            first = self.ss[self.ss.top - 1]
            second = self.ss[self.ss.top]

            name = "EQ"
            if LA == '<':
                name = "LT"
            temp = self.get_temp()
            self.PB[self.i] = f"({name}, {first}, {second}, {temp})"
            self.ss.push(temp)
            self.i += 1

        elif func == "add":
            first = self.ss[self.ss.top - 1]
            second = self.ss[self.ss.top]

            name = "ADD"
            temp = self.get_temp()
            self.PB[self.i] = f"({name}, {first}, {second}, {temp})"
            self.ss.push(temp)
            self.i += 1
        elif func == "mult":
            first = self.ss[self.ss.top - 1]
            second = self.ss[self.ss.top]

            name = "MULT"
            temp = self.get_temp()
            self.PB[self.i] = f"({name}, {first}, {second}, {temp})"
            self.ss.push(temp)
            self.i += 1
        elif func == "negate":
            second = self.ss[self.ss.top]
            temp = self.get_temp()
            self.PB[self.i] = f"(SUB, #0, {second}, {temp})"
            self.i += 1
        elif func == "pushNum":
            self.ss.push(f"#{LA}")
        elif func == "print":

            self.PB[self.i] = f"(PRINT, {self.ss[self.ss.top]}, ,)"
            self.ss.pop(1)
            self.i += 1
    def write_to_file(self):
        f = open("output.txt", "w")

        for i, j in enumerate(self.PB):
            line = str(i) + '\t' + j
            f.write(line)
        f.close()
