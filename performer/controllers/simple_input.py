from .controller import Controller

class SimpleInput(Controller):

    def __init__(self):
        super().__init__()

    def attach(self, item, param, init_value=None):
        if init_value==None: item.get_param(param)
        self.items[item] = {param: init_value}

    def attach_value(self, pointer):
        self.pointer = pointer
        print("ATTACHED", self.pointer)

    def init(self):
        pass
        # self.

    def update(self):
        # TODO: separate this into another controller... this is null controller
        K = float(input("Controller: change freq?"))
        self.write(K)