# authors: Leili Goli 96106044, Mohammad Saneian 96109769

#import sys
from File_Reader import FileReader
from Symbol_Table import SymbolTable

WHITE_SPACE_START_STATES = 29
FINAL_STATES = {5: 'SYMBOL', 9: 'SYMBOL', 10: 'SYMBOL', 11: 'SYMBOL', 12: 'SYMBOL', 13: 'SYMBOL', 14: 'SYMBOL',
                7: 'SYMBOL', 8: 'SYMBOL', 16: 'SYMBOL', 17: 'SYMBOL', 18: 'SYMBOL', 15: 'SYMBOL',
                2: 'IDK', 4: 'NUM', 22: 'COMMENT', 26: 'COMMENT', 27: 'SYMBOL', 28: 'SYMBOL'}


# -1: corrupted identifier, invalid input
# -2: invalid number
# -3: unmatched comment
# -4: unclosed comment
ERROR_MSGS = {-1: "Invalid input", -2: "Invalid number", -3: "Unmatched comment", -4: "Unclosed comment",
              -5: "Invalid input"}


def is_num(c):
    return '0' <= c <= '9'


def id_or_keyword(x):
    if x in "if, else, void, int, while, break, switch, default, case, return, for".split(", "):
        return "KEYWORD"
    return "ID"


def dfa(state, c, next_c):
    all_syms = {'<': 5, ';': 9, ':': 10, ',': 11, '[': 12, ']': 13, '{': 14, '}': 15, '+': 16, '-': 17, '*': 18,
                '(': 27, ')': 28}
    SOW = ";:,[](){}+-*=<\n\r\t\f\v "  # symbol or whitespace
    # print("Processing Symbol: ", c, "lookahead: ", next_c, "State is: ", state)
    if c == 'eof' and not (state == 23 or state == 25):
        return 35
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

    if (state == 0 or state == 3) and is_num(c):
        if next_c in SOW or next_c == 'eof':
            return 4
        elif is_num(next_c):
            return 3
        else:
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

    if state == 0 and c == '/':
        if next_c != '/' and next_c != '*':
            return -5
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
        if c == 'eof':
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
        cnt = 29
        for i in whitespaces:
            if i == c:
                return cnt
            cnt += 1

    return -5


class Scanner():
    def __init__(self, file_reader, symbol_table):
        self.f = file_reader
        self.state = 0
        self.buffer = ""
        self.error_buffer = ""
        self.symbol_table = "if, else, void, int, while, break, switch, default, case, return, for".split(", ")
        self.tokens = {}
        self.errors = {}

        self.symbol_table_with_scoping = symbol_table

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

    def write_lexical_errors(self):
        f = open("lexical_errors.txt", "w")
        if len(self.errors) == 0:
            f.write("There is no lexical error.")

        for i in self.errors.keys():
            line = self.errors[i] + '\n'
            f.write(line)
        f.close()

    def abbr_comment(self, x):

        if len(x) >= 7:
            return x[:7] + "..."
        else:
            return x

    def add_error(self, initial_error_message, line_num):
        if initial_error_message == ERROR_MSGS[-3] or initial_error_message == ERROR_MSGS[-4]:
            self.error_buffer = self.abbr_comment(self.error_buffer)
        if line_num not in self.errors.keys():
            self.errors[line_num] = str(
                line_num) + ".\t(" + self.error_buffer + ", " + initial_error_message + ")"
        else:
            self.errors[line_num] += " (" + self.error_buffer + ", " + initial_error_message + ")"

    def make_token(self, token_type, lexeme):
        return "(" + token_type + ', ' + lexeme + ")"

    def get_next_token(self):

        line_num = 1

        token_value, lexeme = 'sasa', 'lily'

        while True:
            c = self.f.get_next_char()

            if self.state == 0:
                line_num = self.f.lineno
            next_state = dfa(self.state, c, self.f.look_ahead)

            seen_lookahead = [-1, -2, -3, 7]
            flag = False
            if c != 'eof':
                self.buffer += c
            else:
                if next_state != -4:
                    break
                else:
                    flag = True

            if next_state in seen_lookahead:  # == and errors
                self.buffer += self.f.get_next_char()
            lexeme = self.buffer
            self.state = next_state

            go_next = False
            if next_state >= WHITE_SPACE_START_STATES or next_state in FINAL_STATES.keys():

                if next_state in FINAL_STATES.keys():

                    token_type = FINAL_STATES[next_state]

                    if token_type == "IDK":
                        token_type = id_or_keyword(lexeme)
                    if token_type == "ID" and not lexeme in self.symbol_table:
                        self.symbol_table.append(lexeme)
                        self.symbol_table_with_scoping.add_symbol(lexeme)
                    if token_type != "COMMENT":

                        token_value = self.make_token(token_type, lexeme)
                        if line_num not in self.tokens.keys():
                            self.tokens[line_num] = self.make_token(token_type, lexeme)
                        else:
                            self.tokens[line_num] += ' ' + self.make_token(token_type, lexeme)
                        go_next = True
                self.buffer = ""
                self.state = 0

            if next_state >= 0:
                self.error_buffer = ""

            else:
                initial_error_message = ERROR_MSGS[next_state]
                self.error_buffer = self.buffer
                self.add_error(initial_error_message, line_num)
                self.buffer = ""
                self.state = 0
            if go_next or flag:
                break

        if c == 'eof':
            self.write_symboltable()
            self.write_tokens()
            self.write_lexical_errors()
            lexeme = "$"
            token_value = ''
        # print("SCANNER OUTPUT: ", lexeme, token_value)
        return lexeme, token_value


if __name__ == '__main__':
    # f = FileReader(sys.argv[1]+"/input.txt")
    f = FileReader("input.txt")
    symbol_table = SymbolTable()
    s = Scanner(f, symbol_table)
    s.get_next_token()
