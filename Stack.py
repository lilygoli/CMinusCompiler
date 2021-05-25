class Stack:
    def __init__(self):
        self.top = -1
        self.stack = []

    def push(self, x):
        self.stack.append(x)
        self.top += 1

    def pop(self, number):

        self.stack = self.stack[: -number]
        self.top -= number

    def get_element(self, index):

        return self.stack[index]

    def get_top_element(self):
        return self.stack[self.top]

    def get_len(self):
        return len(self.stack)