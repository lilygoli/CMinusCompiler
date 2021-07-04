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
            self.ss.push("@" + str(temp1))
        elif func == "newScope":
            self.symbol_table.new_scope = True
        elif func == "setType":
            self.symbol_table.set_type(LA)
        elif func == "save":
            self.PB += [None]
            self.ss.push(self.i)
            self.i += 1
        elif func == "justSave":
            self.ss.push(0)  # dummy push for alignment with for
            self.ss.push(self.i)
        elif func == "setConditional":
            self.PB[self.ss.get_element(self.ss.top - 1)] = f"(JPF, {self.ss.get_element(self.ss.top - 2)}, {self.i}, )"

        elif func == "setUnconditional":

            self.PB[self.ss.get_element(self.ss.top)] = f"(JP, {self.i}, ,)"

            self.ss.pop(3)

        elif func == "setJump":
            self.PB.append(f"(JP, {self.ss.get_element(self.ss.top - 3)}, ,)")
            self.i += 1
        elif func == "setConditionalFor":

            self.PB[self.ss.get_element(self.ss.top - 1)] = f"(JPF, {self.ss.get_element(self.ss.top - 2)}, {self.i}, )"
            self.ss.pop(4)

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

        elif func == "forTemp":
            temp = self.get_temp()
            self.PB.append(f"(ASSIGN, #0, {temp}, )")
            self.i += 1
            self.ss.push(temp)

        elif func == "saveFor":
            self.PB.append(f"(JP, {self.i + 2}, ,)")
            self.i += 1
            self.PB.append(None)
            self.ss.push(self.i)
            self.i += 1

        elif func == "set":
            self.ss.pop(1)
            self.PB[self.ss.get_element(self.ss.top - 1)] = f"(JP, {self.i + 2}, ,)"
            self.i += 1

        elif func == "for":
            self.PB.append(f"(ADD, {self.ss.get_element(self.ss.top - 4)}, #{1}, {self.ss.get_element(self.ss.top - 4)})")
            self.i += 1
            temp1 = self.get_temp()
            self.PB.append(f"(MULT, #{3}, {self.ss.get_element(self.ss.top - 4)}, {temp1})")
            self.i += 1
            self.PB.append(f"(ADD, {self.ss.get_element(self.ss.top - 1)}, {temp1}, {temp1})")
            self.i += 1
            temp2 = self.get_temp()
            self.PB.append(f"(LT, {self.ss.get_element(self.ss.top - 3)}, {self.ss.get_element(self.ss.top - 4)}, {temp2})")
            self.i += 1
            self.PB.append(f"(JPF, {temp2},{temp1}, )")
            self.i += 1
            self.PB[self.ss.get_element(self.ss.top)] = self.PB.append(f"(JP, {self.i + 1}, ,)")
            self.i += 1
            self.ss.pop(5)

        elif func == "assignFor":
            self.PB.append(f"(ASSIGN, {self.ss.get_element(self.ss.top)}, {self.ss.get_element(self.ss.top - 1)}, )")
            self.i += 1
            self.ss.pop(1)

        elif func == "jumpFor":
            self.PB.append(f"(ADD, {self.ss.get_element(self.ss.top - 3)}, #{1}, {self.ss.get_element(self.ss.top - 3)})")
            self.i += 1
            self.PB.append(f"(JP, {self.ss.get_element(self.ss.top - 2)}, ,)")
            self.i += 1

        elif func == "breakJump":
            self.PB.append(self.PB.append(f"(JP, {self.ss.get_element(self.ss.top)}, ,)"))
            self.i += 1
            self.ss.pop(5)

        # elif func == "pushOr": done
        #     self.ss.push("^")
        #
        # elif func == "loadVal": done
        #     pass
        #
        # elif func == "loadValPrime":
        #     pass
        #
        # elif func == "saveNameForFunc":
        #     pass
        #
        # elif func == "setFuncNameAddr":
        #     pass
        #
        # elif func == "popParams":
        #     pass
        #
        # elif func == "endScope":
        #     self.symbol_table.end_scope()
        #
        # elif func == "pushAnd":
        #     self.ss.push("&")
        #
        # elif func == "saveRet":
        #     self.ss.push(self.i + 1)
        #
        # elif func == "initPush":
        #     self.ss.push(0)
        #
        # elif func == "countPush":
        #     self.ss.push(self.ss.get_element(self.ss.top - 1) + 1)
        #
        # elif func == "jumpFunc":
        #     addr = self.ss.get_element(self.ss.top - self.ss.get_element(self.ss.top) * 2 - 1)
        #     self.PB.append(self.PB.append(f"(JP, @{addr}, ,)"))
        #     self.i += 1
        elif func == "print":

            self.PB.append(f"(PRINT, {self.ss.get_element(self.ss.top)}, ,)")
            self.ss.pop(1)
            self.i += 1
        elif func == "allocFunc":
            funcname = self.ss.get_element(self.ss.top)
            funcAddr = self.symbol_table.find_addr(funcname)
            self.ss.pop(1)
            t = self.get_temp()
            self.PB.append(f"(ASSIGN, #{t}, {funcAddr}, )")
            self.i += 1
            locFunc = t
            addrParam = self.get_temp()
            res = self.get_temp()
            retAddr = self.get_temp()
            self.ss.push(t)
            self.ss.push(self.get_temp())
        elif func == "setParam":
            addr = self.symbol_table.find_addr(LA)
            start = self.ss.get_element(self.ss.top)
            self.PB.append(f"(ASSIGN, #{addr}, {start}, )")
            self.i += 1
            self.ss.pop(1)
            self.ss.push(start + 4)
        elif func == "popFunc":
            self.ss.pop(1)
            top = self.ss.get_element(self.ss.top)
            self.PB.append(f"(ASSIGN, #{self.i + 1}, {top}, )")
            self.i += 1
        elif func == "pushRes":
            start = self.ss.get_element(self.ss.top - 1)
            resAddr = start + 8
            self.PB.append(f"(ASSIGN, #{self.ss.get_element(self.ss.top)}, {resAddr}, )")
            self.i += 1
            self.ss.pop(1)
        elif func == "jumpBack":
            first = self.ss.get_element(self.ss.top)
            ret = first + 12
            self.PB.append(f"(JP, @{ret}, ,)")
            self.i += 1
            self.ss.pop(1)
        elif func == "pushFuncAddr":
            funcAddr = self.symbol_table.find_addr(LA)
            t = self.get_temp()
            self.PB.append(f"(ADD, {funcAddr}, #{12}, {t})")
            self.i += 1
            self.PB.append(f"(ASSIGN, #{self.i + 1}, @{t}, )")
            self.i += 1
            self.ss.push(funcAddr)
        elif func == "setInput":
            func = self.ss.get_element(self.ss.top - 2)
            t = self.get_temp()
            self.PB.append(f"(ADD, {func}, {4}, {t})")
            self.i += 1
            t1 = self.get_temp()
            self.PB.append(f"(ADD, {self.ss.get_element(self.ss.top - 1)}, @{t}, {t1})")
            self.i += 1
            self.PB.append(f"(ASSIGN, #{self.ss.get_element(self.ss.top)}, @{t1}, )")
            self.i += 1
            offset = self.ss.get_element(self.ss.top - 1)
            self.ss.pop(2)
            self.ss.push(offset + 1)
        elif func == "jumpFunc":
            self.ss.pop(1)
            self.PB.append(f"(JP, @{self.ss.get_element(self.ss.top)}, ,)")
            self.i += 1
        elif func == "pushAddrRes":
            funcAddr = self.ss.get_element(self.ss.top)
            t = self.get_temp()
            self.PB.append(f"(ADD, {funcAddr}, #{8}, {t})")
            self.ss.pop(1)
            self.ss.push(t)
    def write_to_file(self):
        f = open("output.txt", "w")

        for i, j in enumerate(self.PB):
            line = str(i) + '\t' + j + '\n'
            f.write(line)
        f.close()
