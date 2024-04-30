


from ai_interface.AI_Interface import AI_Interface


class Module:
    # Robot library stuff
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = "1"

    def __init__(self, name) -> None:
        self.name = name
        self.ai_interface = AI_Interface()