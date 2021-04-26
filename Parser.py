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
        print(f"#{self.line_number}  : syntax error, missing {name}")

    def print_error_illegal(self, LA):
        print(f"#{self.line_number} : syntax error, illegal {LA}")

    def match(self, expected):
        if self.cur_token == expected:
            Node(self.cur_value, parent=self.cur_father_node)
            self.get_next_token()
        else:
            print(f"#{self.line_number}  : Syntax Error, Missing Params")

    def go_next_level(self, func, name):
        node = self.add_edge(name)
        prev_node = self.cur_father_node
        self.cur_father_node = node
        func()
        self.cur_father_node = prev_node

    def Program(self):
        LA = self.cur_token
        if LA in first["Program"]:
            self.go_next_level(self.Declarationlist, "Declaration-list")
        elif LA in follow["Program"]:
            self.print_error_follow("Program")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Program()

    def Declarationlist(self):
        LA = self.cur_token
        if LA in ['int', 'void']:
            self.go_next_level(self.Declaration, "Declaration")
            self.go_next_level(self.Declarationlist, "Declaration-list")
        elif LA in follow["Program"]:
            # epsilon in first
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Declarationlist()

    def Declaration(self):
        LA = self.cur_token
        if LA in first["Declaration"]:
            self.go_next_level(self.Declarationinitial, "Declaration-initial")
            self.go_next_level(self.Declarationprime, "Declaration-prime")
        elif LA in follow["Program"]:
            self.print_error_follow("Declaration")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Declaration()

    def Expression(self):
        LA = self.cur_token
        if LA in ['NUM', '(', '+', '-']:
            self.go_next_level(self.Simpleexpressionzegond, "Simple-expression-zegond")
        elif LA in ['ID']:
            self.match('ID')
            self.go_next_level(self.B, "B")
        elif LA in follow["Expression"]:
            self.print_error_follow("Expression")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Expression()

    def B(self):
        LA = self.cur_token
        if LA in ['=']:
            self.match('=')
            self.go_next_level(self.Expression, "Expression")
        elif LA in ['[']:
            self.match('[')
            self.go_next_level(self.Expression, "Expression")
            self.match(']')
            self.go_next_level(self.H, "H")
        elif LA in ['(', '<', '==', '+', '-', '*']:
            self.go_next_level(self.Simpleexpressionprime, "Simple-expression-prime")
        elif LA in follow["B"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.B()

    def H(self):
        LA = self.cur_token
        if LA in ['=']:
            self.match('=')
            self.go_next_level(self.Expression, "Expression")
        elif LA in ['<', '==', '+', '-', '*']:
            self.go_next_level(self.G, "G")
            self.go_next_level(self.D, "D")
            self.go_next_level(self.C, "C")
        elif LA in follow["H"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.H()

    def Simpleexpressionzegond(self):
        LA = self.cur_token
        if LA in first["Simpleexpressionzegond"]:
            self.go_next_level(self.Additiveexpressionzegond, "Additive-expression-zegond")
            self.go_next_level(self.C, "C")

        elif LA in follow["Simpleexpressionzegond"]:
            self.print_error_follow("Simple-expression-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Simpleexpressionzegond()

    def Simpleexpressionprime(self):
        LA = self.cur_token
        if LA in first["Simpleexpressionzegond"]:
            self.go_next_level(self.Additiveexpressionprime, "Additive-expression-prime")
            self.go_next_level(self.C, "C")

        elif LA in follow["Simpleexpressionprime"]:
            self.print_error_follow("Simple-expression-prime")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Simpleexpressionprime()

    def C(self):
        LA = self.cur_token
        if LA in ['<', '==']:
            self.go_next_level(self.Relop, "Relop")
            self.go_next_level(self.Additiveexpression, "Additive-expression")

        elif LA in follow["C"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.C()

    def Relop(self):
        LA = self.cur_token
        if LA in ['<']:
            self.match('<')
        elif LA in ['==']:
            self.match('==')
        elif LA in follow["Relop"]:
            self.print_error_follow("Relop")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Relop()

    def Additiveexpression(self):
        LA = self.cur_token
        if LA in first["Additiveexpression"]:
            self.go_next_level(self.Term, "Term")
            self.go_next_level(self.D, "D")
        elif LA in follow["Additiveexpression"]:
            self.print_error_follow("Additive-expression")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Additiveexpression()

    def Additiveexpressionprime(self):
        LA = self.cur_token
        if LA in ['(', '+', '-', '*']:
            self.go_next_level(self.Termprime, "Term-prime")
            self.go_next_level(self.D, "D")
        elif LA in follow["Additiveexpressionprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Additiveexpressionprime()

    def Additiveexpressionzegond(self):
        LA = self.cur_token
        if LA in first["Additiveexpressionzegond"]:
            self.go_next_level(self.Termzegond, "Term-zegond")
            self.go_next_level(self.D, "D")
        elif LA in follow["Additiveexpressionzegond"]:
            self.print_error_follow("Additive-expression-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Additiveexpressionzegond()

    def D(self):
        LA = self.cur_token
        if LA in ['+', '-']:
            self.go_next_level(self.Addop, "Addop")
            self.go_next_level(self.Term, "Term")
            self.go_next_level(self.D, "D")
        elif LA in follow["D"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.D()

    def Addop(self):
        LA = self.cur_token
        if LA in ['+', '-']:
            self.match('+')
            self.match('-')
        elif LA in follow["Addop"]:
            self.print_error_follow("Addop")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Addop()

    def Term(self):
        LA = self.cur_token
        if LA in first["Term"]:
            self.go_next_level(self.Signedfactor, "Signed-factor")
            self.go_next_level(self.G, "G")
        elif LA in follow["Term"]:
            self.print_error_follow("Term")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Term()

    def Termprime(self):
        LA = self.cur_token
        if LA in ['(', '*']:
            self.go_next_level(self.Signedfactorprime, "Signed-factor-prime")
            self.go_next_level(self.G, "G")
        elif LA in follow["Termprime"]:
           return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Termprime()

    def Termzegond(self):
        LA = self.cur_token
        if LA in first["Termzegond"]:
            self.go_next_level(self.Signedfactorzegond, "Signed-factor-zegond")
            self.go_next_level(self.G, "G")
        elif LA in follow["Termzegond"]:
            self.print_error_follow("Term-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Termzegond()

    def G(self):
        LA = self.cur_token
        if LA in ['*']:
            self.match('*')
            self.go_next_level(self.Signedfactor, "Signed-factor")
            self.go_next_level(self.G, "G")
        elif LA in follow["G"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.G()

    def Signedfactor(self):
        LA = self.cur_token
        if LA in ['+']:
            self.match('+')
            self.go_next_level(self.Factor, "Factor")
        elif LA in ['-']:
            self.match('-')
            self.go_next_level(self.Factor, "Factor")
        elif LA in ['ID', 'NUM', '(']:
            self.go_next_level(self.Factor, "Factor")
        elif LA in follow["Signedfactor"]:
            self.print_error_follow("Signed-factor")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Signedfactor()

    def Signedfactorprime(self):
        LA = self.cur_token
        if LA in ['(']:
            self.go_next_level(self.Factorprime, "Factor-prime")
        elif LA in follow["Signedfactorprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Signedfactorprime()

    def Signedfactorzegond(self):
        LA = self.cur_token
        if LA in ['+']:
            self.match('+')
            self.go_next_level(self.Factor, "Factor")
        elif LA in ['-']:
            self.match('-')
            self.go_next_level(self.Factor, "Factor")
        elif LA in ['NUM', '(']:
            self.go_next_level(self.Factorzegond, "Factor-zegond")
        elif LA in follow["Signedfactorzegond"]:
            self.print_error_follow("Signed-factor-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Signedfactorzegond()

    def Factor(self):
        LA = self.cur_token
        if LA in ['ID']:
            self.match('ID')
            self.go_next_level(self.Varcallprime, "Var-call-prime")
        elif LA in ['(']:
            self.match('(')
            self.go_next_level(self.Expression, "Expression")
            self.match(')')
        elif LA in ['NUM']:
            self.match('NUM')
        elif LA in follow["Factor"]:
            self.print_error_follow("Factor")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Factor()

    def Varcallprime(self):
        LA = self.cur_token
        if LA in ['(']:
            self.match('(')
            self.go_next_level(self.Args, "Args")
            self.match(')')
        elif LA in ['[']:
            self.go_next_level(self.Varprime, "Var-prime")
        elif LA in follow["Varcallprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Varcallprime()

    def Varprime(self):
        LA = self.cur_token
        if LA in ['[']:
            self.match('[')
            self.go_next_level(self.Expression, "Expression")
            self.match(']')

        elif LA in follow["Varprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Varprime()

    def Factorprime(self):
        LA = self.cur_token
        if LA in ['(']:
            self.match('(')
            self.go_next_level(self.Args, "Args")
            self.match(')')
        elif LA in follow["Factorprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Factorprime()

    def Factorzegond(self):
        LA = self.cur_token
        if LA in ['(']:
            self.match('(')
            self.go_next_level(self.Expression, "Expression")
            self.match(')')
        elif LA in ['NUM']:
            self.match('NUM')
        elif LA in follow["Factorzegond"]:
            self.print_error_follow("Factor-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Factorzegond()

    def Args(self):
        LA = self.cur_token
        if LA in ['ID', 'NUM', '(', '+', '-']:
            self.go_next_level(self.Arglist, "Arg-list")
        elif LA in follow["Args"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Args()

    def Arglist(self):
        LA = self.cur_token
        if LA in first['Arglist']:
            self.go_next_level(self.Expression, "Expression")
            self.go_next_level(self.Arglistprime, "Arg-list-prime")
        elif LA in follow["Arglist"]:
            self.print_error_follow("Arg-list")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Arglist()

    def Arglistprime(self):
        LA = self.cur_token
        if LA in [',']:
            self.match(',')
            self.go_next_level(self.Expression, "Expression")
            self.go_next_level(self.Arglistprime, "Arg-list-prime")
        elif LA in follow["Arglistprime"]:
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Arglistprime()

def give_googooli(x):
    print("first of " + x + " is: ")
    print(first[x])
    print("follow of " + x + " is: ")
    print(follow[x])


x = 'Arglistprime'

give_googooli(x)
if __name__ == '__main__':
    f = FileReader("test.txt")
    s = Scanner(f)
    next = ''
    while next != "$":
        next = s.get_next_token()[0]

    # root = Node("Program")
    # p = Parser(s, root)
    # p.Program()
