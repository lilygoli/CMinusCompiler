from File_Reader import FileReader

final_states = {5: 'SYMBOL', 9: 'SYMBOL', 10: 'SYMBOL', 11: 'SYMBOL', 12: 'SYMBOL', 13: 'SYMBOL', 14: 'SYMBOL',
                7: 'SYMBOL', 8: 'SYMBOL', 16: 'SYMBOL', 17: 'SYMBOL', 18: 'SYMBOL', 15: 'SYMBOL',
                2: 'ID', 4: 'NUM', 22: 'COMMENT', 26: 'COMMENT'}


# print(final_states)
# -1: identifier kharab shode, invalid input
# -2: invalid number
# -3: unmatched comment
# -4: unclosed comment

def is_num(c):
    return '0' <= c <= '9'


def dfa(state, c, next_c):
    all_syms = {'<': 5, ';': 9, ':': 10, '[': 12, ']': 13, '{': 14, '}': 15, '+': 16, '-': 17, '*': 18}
    SOW = ";:,[](){}+-*=<\n\r\t\f\v "  # symbol or whitespace
    # print("Processing Symbol: ", c, "lookahead: ", next_c, "State is: ", state)
    if c == 'eof':
        return 33
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
    # NUM DFA

    if (state == 0 or state == 3) and is_num(c):
        if next_c in SOW or next_c == 'eof':
            return 4
        elif is_num(next_c):
            return 1
        else:
            # TODO
            return -2
    # Comment DFA
    if state == '0' and c == '/':
        return 19
    if state == 19:
        if c == '/':
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
        elif c == '/':
            return 26
        else:
            return 23

    whitespaces = '\n\r\t\f\v '

    if state == 0 and c in whitespaces:
        cnt = 27
        for i in whitespaces:
            if i == c:
                return cnt
            cnt += 1
    # print(state, c, next_c)
    print("OH NO")


# -1: identifier kharab shode, invalid input
# -2: invalid number
# -3: unmatched comment
# -4: unclosed comment
error_msg = {-1: "invalid input", -2: "invalid number", -3: "unmatched comment", 4: "unclosed comment"}


class Scanner():
    def __init__(self, file_reader):
        self.f = file_reader
        self.state = 0
        self.buffer = ""
        self.errors = ""

    def scan(self):

        while True:

            c = self.f.get_next_char()
            next_state = dfa(self.state, c, self.f.look_ahead)
            self.buffer += c
            prev_state = self.state
            self.state = next_state
            # print(next_state)
            if next_state >= 27 or next_state in final_states.keys():
                st = "lexeme: " +self.buffer + ", " + "line: "+ str(self.f.lineno)
                if next_state in final_states.keys():
                    st += ", Type: " + final_states[next_state]
                    print(st, ", curr state: ", next_state, ", prev state: ", prev_state)
                else:
                    print(st, ", curr state",", Type: WHITESPACE ", next_state, ", prev state: ", prev_state)
                self.buffer = ""
                self.state = 0
            if next_state < 0:  # error
                print(error_msg[next_state])
                # self.errors += error_msg[next_state] + " " + self.f.lineno #todo handle error log
                self.errors += self.buffer
                self.buffer = ""
                self.state = 0

            if c == 'eof':
                break


if __name__ == '__main__':
    f = FileReader("test.txt")
    s = Scanner(f)
    s.scan()
