class FileReader:
    def __init__(self, path):
        self.path = path
        self.lineno = 0
        self.cur_char = ''
        self.look_ahead = ''
        self.cur_line = ''
        self.file = None
        self.get_next_line()

    def get_next_line(self):
        if not self.file:
            self.file = open(self.path, "r")
        self.cur_line = self.file.readline()
        self.lineno += 1

    def get_cur_char(self):
        return self.cur_char

    def get_next_char(self):
        if self.cur_line == '':
            self.get_next_line()
        if not self.cur_line:
            return 'eof'
        self.cur_char = self.cur_line[0]
        if len(self.cur_line) <= 1:
            self.look_ahead = None
        else:
            self.look_ahead = self.cur_line[1]
        self.cur_line = self.cur_line[1:]
        return self.cur_char


# testing

f = FileReader("./test.txt")
while f.get_next_char() != 'eof':
    print(f.get_next_char(), f.lineno)
