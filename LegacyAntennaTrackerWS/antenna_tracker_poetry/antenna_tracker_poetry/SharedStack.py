class SharedStack:
    def __init__(self, length):
        self.latest = None
        self.stack = []
        self.length = length

    def push(self, item):
        self.stack.append(item)
        self.latest = item
        print(f"Pushed {item} to stack")

    def pop(self):
        if len(self.stack) > 0:
            item = self.stack.pop()
            return item
        else:
            print("Stack is empty")
            return None

    def peek(self, index):
        return self.latest
        # if 0 <= index < len(self.stack):
        #     return self.stack[index]
        # else:
        #     print(f"Index {index} is out of bounds")
        #     return None