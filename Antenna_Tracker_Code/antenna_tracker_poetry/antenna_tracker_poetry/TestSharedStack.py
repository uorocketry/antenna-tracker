class TestSharedStack:
    def __init__(self, length):
        self.stack = []
        self.length = length

    def push(self, item):
        if len(self.stack) >= self.length:
            self.stack.pop(0)  # Remove the oldest item (at index 0)
        self.stack.append(item)
        print(f"Pushed {item} to stack")

    def pop(self):
        if len(self.stack) > 0:
            item = self.stack.pop()
            print(f"Popped {item} from stack")
            return item
        else:
            print("Stack is empty")
            return None

    def peek(self, index):
        if 0 <= index < len(self.stack):
            return self.stack[index]
        else:
            # print(f"Index {index} is out of bounds")
            return None