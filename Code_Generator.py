# authors: Mohammad Saneian 96109769 Leili Goli 96106044

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
        elif func == "getElement":

            second = self.ss.get_element(self.ss.top)
            temp = self.get_temp()
            self.PB.append(f"(MULT, {second}, #{4}, {temp})")
            self.i += 1
            self.ss.pop(1)
            self.ss.push(temp)
            temp1 = self.get_temp()

            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)
            name = "ADD"
            self.PB.append(f"({name}, #{first}, {second}, {temp1})")
            self.i += 1
            self.ss.pop(2)
            self.ss.push("@"+str(temp1))
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
            self.PB[self.ss.get_element(self.ss.top - 1)] = f"(JPF, {self.ss.get_element(self.ss.top - 2)}, {self.i}, )"

        elif func == "setUnconditional":

            self.PB[self.ss.get_element(self.ss.top)] = f"(JP, {self.i}, ,)"

            self.ss.pop(3)

        elif func == "setJump":
            self.PB.append(f"(JP, {self.ss.get_element(self.ss.top - 2)}, ,)")
            self.i += 1
        elif func == "setConditionalFor":

            self.PB[self.ss.get_element(self.ss.top)] = f"(JPF, {self.ss.get_element(self.ss.top - 1)}, {self.i}, )"
            self.ss.pop(3)


        elif func == "compare_LT":
            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)

            temp = self.get_temp()
            self.PB.append(f"(LT, {first}, {second}, {temp})")
            self.ss.pop(2)
            self.ss.push(temp)
            self.i += 1
        elif func == "compare_EQ":
            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)

            temp = self.get_temp()
            self.PB.append(f"(EQ, {first}, {second}, {temp})")
            self.ss.pop(2)
            self.ss.push(temp)
            self.i += 1

        elif func == "add":
            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)

            name = "ADD"
            temp = self.get_temp()
            self.PB.append(f"({name}, {first}, {second}, {temp})")
            self.ss.pop(2)
            self.ss.push(temp)
            self.i += 1
        elif func == "sub":
            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)

            name = "SUB"
            temp = self.get_temp()
            self.PB.append(f"({name}, {first}, {second}, {temp})")
            self.ss.pop(2)
            self.ss.push(temp)
            self.i += 1
        elif func == "mult":
            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)

            name = "MULT"
            temp = self.get_temp()
            self.PB.append(f"({name}, {first}, {second}, {temp})")
            self.ss.pop(2)
            self.ss.push(temp)
            self.i += 1
        elif func == "negate":
            second = self.ss.get_element(self.ss.top)
            temp = self.get_temp()
            self.PB.append(f"(SUB, #0, {second}, {temp})")
            self.ss.pop(1)
            self.ss.push(temp)
            self.i += 1
        elif func == "pushNum":
            temp = self.get_temp()
            self.PB.append(f"(ASSIGN, #{LA}, {temp}, )")
            self.i += 1
            self.ss.push(temp)
        elif func == "assign":

            first = self.ss.get_element(self.ss.top - 1)
            second = self.ss.get_element(self.ss.top)
            self.PB.append(f"(ASSIGN, {second}, {first}, )")
            self.ss.pop(1)
            self.i += 1

        elif func == "pop":
            self.ss.pop(1)

        elif func == "print":

            self.PB.append(f"(PRINT, {self.ss.get_element(self.ss.top)}, ,)")
            self.ss.pop(1)
            self.i += 1

    def write_to_file(self):
        f = open("output.txt", "w")

        for i, j in enumerate(self.PB):
            line = str(i) + '\t' + j + '\n'
            f.write(line)
        f.close()
