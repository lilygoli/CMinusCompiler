from anytree import Node

from Code_Generator import CodeGenerator
from File_Reader import FileReader
from Parser import Parser, write_parse_files
from Scanner import Scanner
from Symbol_Table import SymbolTable

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