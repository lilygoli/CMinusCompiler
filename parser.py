from File_Reader import FileReader
from Scanner import Scanner
from anytree import Node, RenderTree


def get_dictionary(file_name):
    # first_sets, follow_sets, predicate_sets
    name = "parserdata/" + file_name + ".txt"
    file = open(name, 'r')

    Lines = file.readlines()
    count = 0
    tokens = []
    info = {}
    for line in Lines:
        count += 1
        s = line.strip()
        if count == 1:
            tokens = s.split("\t")
        else:
            a = s.split("\t")
            rule_id = a[0]
            l = []
            for i in range(1, len(a)):
                if a[i] == "+":
                    l.append(tokens[i - 1])
            info[rule_id] = l
    return info


first = get_dictionary("first_sets")
follow = get_dictionary("follow_sets")

# lili_command = ["B", "H", "Statement", "Statementlist"]
#
# for i in lili_command:
#     print(i, "__________")
#     print("first set is")
#     print(first[i])
#     print("follow set is")
#     print(follow[i])


class Parser():
    def __init__(self, scanner):
        self.scanner = scanner
        self.line_number = 0
        self.cur_token = ''
        self.get_next_token()

    def get_next_token(self):
        self.cur_token = self.scanner.get_next_token()
        self.line_number = self.scanner.f.lineno

    def add_edge(self, a, b):
        Node(b, parent=a)

    def print_error_follow(self, name):
        print("missing" + name + " in line " + self.line_number)

    def print_error_illegal(self, LA):
        print("illegal" + LA + " in line " + self.line_number)

    def match(self, expected):
        if self.cur_token == expected:
            self.get_next_token()
        else:
            print("missing "+ expected + " in line "+ self.line_number)

    def Program(self):
        LA = self.cur_token
        if LA in first["Program"]:
            self.add_edge("Declaration_list", "Program")
            self.Declaration_list()
        elif LA in follow["Program"]:
            self.print_error_follow("Program")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()

    def Declaration_list(self):
        pass


f = FileReader("test.txt")
s = Scanner(f)
p = Parser(s)
Node("Program")
p.Program()
