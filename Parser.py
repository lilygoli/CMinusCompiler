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
    def __init__(self, scanner, start):
        self.scanner = scanner
        self.line_number = 0
        self.cur_token = ''
        self.cur_value = ''
        self.get_next_token()
        self.cur_father_node = start

    def get_next_token(self):
        self.cur_token, self.cur_value = self.scanner.get_next_token()
        self.line_number = self.scanner.f.lineno

    def add_edge(self, b):
        return Node(b, parent=self.cur_father_node)

    def print_error_follow(self, name):
        print("missing" + name + " in line " + self.line_number)

    def print_error_illegal(self, LA):
        print("illegal" + LA + " in line " + self.line_number)

    def match(self, expected):
        if self.cur_token == expected:
            Node(self.cur_value, parent=self.cur_father_node)
            self.get_next_token()
        else:
            print("missing "+ expected + " in line "+ self.line_number)

    def go_next_level(self, func, name):
        node = self.add_edge(name)
        prev_node = self.cur_father_node
        self.cur_father_node = node
        func()
        self.cur_father_node = prev_node

    def Program(self):
        LA = self.cur_token
        if LA in first["Program"]:
            self.go_next_level(self.Declaration_list, "Declaration_list")
        elif LA in follow["Program"]:
            self.print_error_follow("Program")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Program()

    def Declaration_list(self):
        pass


if __name__ == '__main__':
    f = FileReader("test.txt")
    s = Scanner(f)
    # next = ''
    # while next != "$":
    #     next = s.get_next_token()[0]

    root = Node("Program")
    p = Parser(s, root)
    p.Program()
