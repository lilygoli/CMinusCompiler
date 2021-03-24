from File_Reader import FileReader

final_states = {5: 'SYMBOL', 9: 'SYMBOL', 10: 'SYMBOL', 11: 'SYMBOL', 12: 'SYMBOL', 13: 'SYMBOL', 14: 'SYMBOL',
                7: 'SYMBOL', 8: 'SYMBOL', 16: 'SYMBOL', 17: 'SYMBOL', 18: 'SYMBOL', 15: 'SYMBOL',
                2: 'IDK', 4: 'NUM', 22: 'COMMENT', 26: 'COMMENT', 27: 'SYMBOL', 28: 'SYMBOL'}

remaning = 2
# print(final_states)
# -1: identifier kharab shode, invalid input
# -2: invalid number
# -3: unmatched comment
# -4: unclosed comment

def is_num(c):
    return '0' <= c <= '9'

def id_or_keyword(x):
    if x in "if, else, void, int, while, break, switch, default, case, return, for".split(", "):
        return "KEYWORD"
    return "ID"

def dfa(state, c, next_c):
    all_syms = {'<': 5, ';': 9, ':': 10,',': 11, '[': 12, ']': 13, '{': 14, '}': 15, '+': 16, '-': 17, '*': 18, '(':27, ')': 28}
    SOW = ";:,[](){}+-*=<\n\r\t\f\v "  # symbol or whitespace
    print("Processing Symbol: ", c, "lookahead: ", next_c, "State is: ", state)
    if c == 'eof':
        return 33 + remaning
    if state == 0 and c in all_syms.keys():

        if c == '*':
            if next_c != '/':
                return all_syms[c]
            else:
                return -3
        else:
            return all_syms[c]

    if state == 0 and c == '=' and next_c == '=':
        return 7
    if state == 0 and c == '=':
        return 8

    # NUM DFA
    print(c, c.isalpha())
    if (state == 0 or state == 3) and is_num(c):
        if next_c in SOW or next_c == 'eof':
            return 4
        elif is_num(next_c):
            return 3
        else:
            # TODO
            return -2
    # ID DFA

    if state == 0 and c.isalpha():
        if next_c in SOW or next_c == 'eof':
            return 2
        elif next_c.isalnum():
            return 1
        else:
            return -1
    if state == 1:
        if next_c in SOW or next_c == 'eof':
            return 2
        elif next_c.isalnum():
            return 1
        else:
            return -1

    # Comment DFA
    x = chr(47)
    if state == 0 and c == x:
        return 19
    if state == 19:
        if c == x:
            return 20
        elif c == '*':
            return 23
    if state == 20:
        if c != '\n':
            return 20
        if c == '\n':
            return 22
    if state == 23 or state == 25:
        if next_c == 'eof':
            return -4
    if state == 23:
        if c != '*':
            return 23
        else:
            return 25
    if state == 25:
        if c == '*':
            return 25
        elif c == x:
            return 26
        else:
            return 23

    whitespaces = '\n\r\t\f\v '

    if state == 0 and c in whitespaces:
        cnt = 27 + remaning
        for i in whitespaces:
            if i == c:
                return cnt
            cnt += 1
    # print(state, c, next_c)
    print("OH NO, Oh no, Oh no no no no no")
    return -5

# -1: identifier kharab shode, invalid input
# -2: invalid number
# -3: unmatched comment
# -4: unclosed comment
error_msg = {-1: "invalid input", -2: "invalid number", -3: "unmatched comment", -4: "unclosed comment", -5: "invalid input"}


class Scanner():
    def __init__(self, file_reader):
        self.f = file_reader
        self.state = 0
        self.buffer = ""
        self.errors = ""
        self.symbol_table = "if, else, void, int, while, break, switch, default, case, return, for".split(", ")
        self.tokens = {}
    def write_symboltable(self):
        f = open("symbol_table.txt", "w")
        for i, line in enumerate(self.symbol_table):
            line = str(i + 1) + ".\t" + line + '\n'
            f.write(line)
        f.close()
    def write_tokens(self):
        f = open("tokens.txt", "w")
        for i in self.tokens.keys():
            line = str(i) + ".\t" + self.tokens[i] + '\n'
            f.write(line)
        f.close()
    def make_token(self,token_type, lexeme):
        return "( " + token_type + ', ' + lexeme + ")"
    def scan(self):

        while True:

            c = self.f.get_next_char()
            next_state = dfa(self.state, c, self.f.look_ahead)
            seen_lookahead = [7, -2, -1, -3, -5]
            if next_state in seen_lookahead: # ==, invalid number
                self.buffer += self.f.get_next_char()
            self.buffer += c
            lexeme = self.buffer
            line_num = self.f.lineno
            prev_state = self.state
            self.state = next_state
            if next_state >= (27 + remaning) or next_state in final_states.keys():
                st = "lexeme: " +self.buffer + "\t " + "line: "+ str(self.f.lineno)
                if next_state in final_states.keys():
                    token_type = final_states[next_state]

                    if token_type == "IDK":
                        token_type = id_or_keyword(lexeme)
                    if token_type == "ID" and not lexeme in self.symbol_table:
                        self.symbol_table.append(lexeme)
                    if not line_num in self.tokens.keys():
                        self.tokens[line_num] = self.make_token(token_type, lexeme)
                    else:
                        self.tokens[line_num] += ' ' + self.make_token(token_type, lexeme)
                    st += " Type: " + token_type
                    print(st, "\tcurr state: ", next_state, "\tprev state: ", prev_state)
                else:
                    print(st, "\tcurr state",", Type: WHITESPACE ", next_state, "\tprev state: ", prev_state)
                self.buffer = ""
                self.state = 0
            if next_state < 0:  # error
                print(error_msg[next_state])
                # self.errors += error_msg[next_state] + " " + self.f.lineno #todo handle error log
                self.errors += self.buffer
                self.buffer = ""
                self.state = 0

            if c == 'eof':
                self.write_symboltable()
                self.write_tokens()
                break


if __name__ == '__main__':
    f = FileReader("test.txt")
    s = Scanner(f)
    s.scan()
