



from ai_interface.AI_Interface import AI_Interface


class Module:

    def __init__(self, name) -> None:
        self.name = name
        self.ai_interface = AI_Interface()