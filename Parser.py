# authors: Mohammad Saneian 96109769 Leili Goli 96106044

from Code_Generator import CodeGenerator
from File_Reader import FileReader
from Scanner import Scanner
from anytree import Node, RenderTree

from Symbol_Table import SymbolTable


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


class Parser():
    def __init__(self, scanner, start, code_gen):
        self.scanner = scanner
        self.line_number = 0
        self.cur_token = ''
        self.cur_value = ''
        self.get_next_token()
        self.cur_father_node = start
        self.root = start
        self.errors = ''
        self.code_generator = code_gen

    def get_next_token(self):
        self.cur_token, self.cur_value = self.scanner.get_next_token()
        if '(ID,' in self.cur_value:
            self.cur_token = 'ID'
        if 'NUM, ' in self.cur_value:
            self.cur_token = 'NUM'
        self.line_number = self.scanner.f.lineno

    def add_edge(self, b):
        return Node(b, parent=self.cur_father_node)

    def remove_node(self):
        parent = self.cur_father_node.parent
        children = list(parent.children)
        children.remove(self.cur_father_node)
        parent.children = children

    def write_string(self, f, string):
        f = open(f, "w")
        f.write(string)
        f.close()

    def print_error_follow(self, name):
        self.errors += f"#{self.line_number}  : syntax error, missing {name}\n"

    def print_error_illegal(self, LA):
        if LA == "$":
            self.remove_node()
            self.errors += f"#{self.line_number} : syntax error, unexpected EOF\n"
            tree = ''
            for pre, fill, node in RenderTree(self.root):  # write to file
                tree += "%s%s\n" % (pre, node.name)
            self.write_string("syntax_errors.txt", self.errors)
            self.write_string("parse_tree.txt", tree)
            exit()
        else:
            self.errors += f"#{self.line_number} : syntax error, illegal {LA}\n"

    def match(self, expected):
        if self.cur_token == expected:
            Node(self.cur_value, parent=self.cur_father_node)
            self.get_next_token()
        else:
            self.errors += f"#{self.line_number}  : syntax error, missing {expected}\n"

    def epsilon_child(self):
        Node("epsilon", parent=self.cur_father_node)

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
            self.remove_node()
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
        elif LA in follow["Declarationlist"]:
            self.epsilon_child()

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
        elif LA in follow["Declaration"]:
            self.remove_node()
            self.print_error_follow("Declaration")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Declaration()

    def Declarationinitial(self):
        LA = self.cur_token
        if LA in first["Declarationinitial"]:
            self.go_next_level(self.Typespecifier, "Type-specifier")
            self.match(self.cur_token)
        elif LA in follow["Declarationinitial"]:
            self.remove_node()
            self.print_error_follow("Declaration-initial")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Declarationinitial()

    def Declarationprime(self):
        LA = self.cur_token
        if LA in ['(']:
            self.go_next_level(self.Fundeclarationprime, "Fun-declaration-prime")
        elif LA in first["Declarationprime"]:
            self.go_next_level(self.Vardeclarationprime, "Var-declaration-prime")
        elif LA in follow["Declarationprime"]:
            self.remove_node()
            self.print_error_follow("Declaration-prime")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Declarationprime()

    def Vardeclarationprime(self):
        LA = self.cur_token
        if LA in [';']:
            self.match(';')
        elif LA in ['[']:
            self.match('[')
            self.match('NUM')
            self.match(']')
            self.match(';')
        elif LA in follow["Vardeclarationprime"]:
            self.remove_node()
            self.print_error_follow("Var-declaration-prime")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Vardeclarationprime()

    def Fundeclarationprime(self):
        LA = self.cur_token
        if LA in first["Fundeclarationprime"]:
            self.match('(')
            self.go_next_level(self.Params, "Params")
            self.match(')')
            self.go_next_level(self.Compoundstmt, "Compound-stmt")
        elif LA in follow["Fundeclarationprime"]:
            self.remove_node()
            self.print_error_follow("Fun-declaration-prime")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Fundeclarationprime()

    def Typespecifier(self):
        LA = self.cur_token
        if LA in first["Typespecifier"]:
            self.match(LA)
        elif LA in follow["Typespecifier"]:
            self.remove_node()
            self.print_error_follow("Type-specifier")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Typespecifier()

    def Params(self):
        LA = self.cur_token
        if LA in ['int']:
            self.match('int')
            self.match(self.cur_token)
            self.go_next_level(self.Paramprime, "Param-prime")
            self.go_next_level(self.Paramlist, "Param-list")
        elif LA in ['void']:
            self.match('void')
            self.go_next_level(self.Paramlistvoidabtar, "Param-list-void-abtar")
        elif LA in follow["Params"]:
            self.remove_node()
            self.print_error_follow("Params")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Params()

    def Paramlistvoidabtar(self):
        LA = self.cur_token
        if LA in ['ID']:
            self.match(self.cur_token)
            self.go_next_level(self.Paramprime, "Param-prime")
            self.go_next_level(self.Paramlist, "Param-list")
        elif LA in follow["Paramlistvoidabtar"]:
            self.epsilon_child()
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Paramlistvoidabtar()

    def Paramlist(self):
        LA = self.cur_token
        if LA in [',']:
            self.match(',')
            self.go_next_level(self.Param, "Param")
            self.go_next_level(self.Paramlist, "Param-list")
        elif LA in follow["Paramlist"]:
            self.epsilon_child()
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Paramlist()

    def Param(self):
        LA = self.cur_token
        if LA in first['Param']:
            self.go_next_level(self.Declarationinitial, "Declaration-initial")
            self.go_next_level(self.Paramprime, "Param-prime")
        elif LA in follow["Param"]:
            self.remove_node()
            self.print_error_follow("Param")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Param()

    def Paramprime(self):
        LA = self.cur_token
        if LA in first['Paramprime']:
            self.match('[')
            self.match(']')
        elif LA in follow["Paramprime"]:
            self.epsilon_child()
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Paramprime()

    def Compoundstmt(self):
        LA = self.cur_token
        if LA in first['Compoundstmt']:
            self.match('{')
            self.go_next_level(self.Declarationlist, "Declaration-list ")
            self.go_next_level(self.Statementlist, "Statement-list")
            self.match('}')
        elif LA in follow["Compoundstmt"]:
            self.remove_node()
            self.print_error_follow("Compound-stmt")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Compoundstmt()

    def Statementlist(self):
        LA = self.cur_token
        if LA in first['Statementlist']:
            self.go_next_level(self.Statement, "Statement")
            self.go_next_level(self.Statementlist, "Statement-list")
        elif LA in follow["Statementlist"]:
            self.epsilon_child()
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Statementlist()

    def Statement(self):
        LA = self.cur_token
        if LA in ['{']:
            self.go_next_level(self.Compoundstmt, "Compound-stmt")
        elif LA in ['if']:
            self.go_next_level(self.Selectionstmt, "Selection-stmt")
        elif LA in ['while']:
            self.go_next_level(self.Iterationstmt, "Iteration-stmt")
        elif LA in ['return']:
            self.go_next_level(self.Returnstmt, "Return-stmt")
        elif LA in ['for']:
            self.go_next_level(self.Forstmt, "For-stmt")
        elif LA in first['Statement']:
            self.go_next_level(self.Expressionstmt, "Expression-stmt")
        elif LA in follow['Statement']:
            self.remove_node()
            self.print_error_follow("Statement")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Statement()

    def Expressionstmt(self):
        LA = self.cur_token
        if LA in ['break']:
            self.match('break')
            self.match(';')
        elif LA in [';']:
            self.match(';')
        elif LA in first['Expressionstmt']:
            self.go_next_level(self.Expression, "Expression")
            self.match(';')
        elif LA in follow['Expressionstmt']:
            self.remove_node()
            self.print_error_follow('Expression-stmt')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Expressionstmt()

    def Selectionstmt(self):
        LA = self.cur_token
        if LA in first['Selectionstmt']:
            self.match('if')
            self.match('(')
            self.go_next_level(self.Expression, "Expression")
            self.match(')')
            self.go_next_level(self.Statement, "Statement")
            self.match('else')
            self.go_next_level(self.Statement, "Statement")
        elif LA in follow['Selectionstmt']:
            self.remove_node()
            self.print_error_follow('Selection-stmt')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Selectionstmt()

    def Iterationstmt(self):
        LA = self.cur_token
        if LA in first['Iterationstmt']:
            self.match('while')
            self.match('(')
            self.go_next_level(self.Expression, "Expression")
            self.match(')')
            self.go_next_level(self.Statement, "Statement")
        elif LA in follow['Iterationstmt']:
            self.remove_node()
            self.print_error_follow('Iteration-stmt')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Iterationstmt()

    def Returnstmt(self):
        LA = self.cur_token
        if LA in first['Returnstmt']:
            self.match('return')
            self.go_next_level(self.Returnstmtprime, "Return-stmt-prime")
        elif LA in follow['Returnstmt']:
            self.remove_node()
            self.print_error_follow('Return-stmt')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Returnstmt()

    def Returnstmtprime(self):
        LA = self.cur_token
        if LA in [';']:
            self.match(';')
        elif LA in first['Returnstmtprime']:
            self.go_next_level(self.Expression, "Expression")
            self.match(';')
        elif LA in follow['Returnstmtprime']:
            self.remove_node()
            self.print_error_follow('Return-stmt-prime')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Returnstmtprime()

    def Forstmt(self):
        LA = self.cur_token
        if LA in first['Forstmt']:
            self.match('for')
            self.match(self.cur_token)
            self.match('=')
            self.go_next_level(self.Vars, "Vars")
            self.go_next_level(self.Statement, "Statement")
        elif LA in follow['Forstmt']:
            self.remove_node()
            self.print_error_follow('For-stmt')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Forstmt()

    def Vars(self):
        LA = self.cur_token
        if LA in first['Vars']:
            self.go_next_level(self.Var, "Var")
            self.go_next_level(self.Varzegond, "Var-zegond")
        elif LA in follow['Vars']:
            self.remove_node()
            self.print_error_follow('Vars')
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Vars()

    def Varzegond(self):
        LA = self.cur_token
        if LA in first['Varzegond']:
            self.match(',')
            self.go_next_level(self.Var, "Var")
            self.go_next_level(self.Varzegond, "Var-zegond")
        elif LA in follow['Varzegond']:
            self.epsilon_child()
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Varzegond()

    def Var(self):
        LA = self.cur_token
        if LA in first['Var']:
            self.match(self.cur_token)
            self.go_next_level(self.Varprime, "Var-prime")
        elif LA in follow['Var']:
            self.remove_node()
            self.print_error_follow("Var")
            return
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Var()

    def Expression(self):
        LA = self.cur_token
        if LA in ['NUM', '(', '+', '-']:
            self.go_next_level(self.Simpleexpressionzegond, "Simple-expression-zegond")
        elif LA in ['ID']:
            self.match(self.cur_token)
            self.go_next_level(self.B, "B")
        elif LA in follow["Expression"]:
            self.remove_node()
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
            self.go_next_level(self.Simpleexpressionprime, "Simple-expression-prime")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.B()

    def H(self):
        LA = self.cur_token
        if LA in ['=']:
            self.match('=')
            self.go_next_level(self.Expression, "Expression")
        elif LA in ['<', '==', '+', '-', '*'] or LA in follow["H"]:
            self.go_next_level(self.G, "G")
            self.go_next_level(self.D, "D")
            self.go_next_level(self.C, "C")
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
            self.remove_node()
            self.print_error_follow("Simple-expression-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Simpleexpressionzegond()

    def Simpleexpressionprime(self):  # here
        LA = self.cur_token

        if LA in first["Simpleexpressionprime"]:
            self.go_next_level(self.Additiveexpressionprime, "Additive-expression-prime")
            self.go_next_level(self.C, "C")
        elif LA in follow["Simpleexpressionprime"]:
            self.go_next_level(self.Additiveexpressionprime, "Additive-expression-prime")
            self.go_next_level(self.C, "C")
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
            self.epsilon_child()
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
            self.remove_node()
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
            self.remove_node()
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
            self.go_next_level(self.Termprime, "Term-prime")
            self.go_next_level(self.D, "D")
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
            self.remove_node()
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
            self.epsilon_child()
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.D()

    def Addop(self):
        LA = self.cur_token
        if LA in ['+']:
            self.match('+')
        elif LA in ['-']:
            self.match('-')
        elif LA in follow["Addop"]:
            self.remove_node()
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
            self.remove_node()
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
            self.go_next_level(self.Signedfactorprime, "Signed-factor-prime")
            self.go_next_level(self.G, "G")
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
            self.remove_node()
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

            self.epsilon_child()
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
            self.remove_node()
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
            self.go_next_level(self.Factorprime, "Factor-prime")
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
            self.remove_node()
            self.print_error_follow("Signed-factor-zegond")
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Signedfactorzegond()

    def Factor(self):
        LA = self.cur_token
        if LA in ['ID']:
            self.match(self.cur_token)
            self.go_next_level(self.Varcallprime, "Var-call-prime")
        elif LA in ['(']:
            self.match('(')
            self.go_next_level(self.Expression, "Expression")
            self.match(')')
        elif LA in ['NUM']:
            self.match('NUM')
        elif LA in follow["Factor"]:
            self.remove_node()
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
            self.go_next_level(self.Varprime, "Var-prime")
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
            self.epsilon_child()
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
            self.epsilon_child()
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
            self.remove_node()
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
            self.epsilon_child()
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
            self.remove_node()
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
            self.epsilon_child()
        else:
            self.print_error_illegal(LA)
            self.get_next_token()
            self.Arglistprime()


def write_parse_files(p):
    tree = ''
    for pre, fill, node in RenderTree(p.root):
        tree += "%s%s\n" % (pre, node.name)
    if p.errors == '':
        p.errors = 'There is no syntax error.'
    p.write_string("syntax_errors.txt", p.errors)
    p.write_string("parse_tree.txt", tree)


if __name__ == '__main__':
    f = FileReader("input.txt")
    symbol_table = SymbolTable()
    s = Scanner(f, symbol_table)
    code_generator = CodeGenerator(symbol_table)

    root = Node("Program")
    p = Parser(s, root, code_generator)
    p.Program()
    p.add_edge("$")

    write_parse_files(p)
