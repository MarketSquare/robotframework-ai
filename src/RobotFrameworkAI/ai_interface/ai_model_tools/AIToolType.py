class AIToolType():
    """
    Interface for all tool types

    This class defines the common methods and attributes that all AI tool types must implement.
    AI tool types are types of tools, such as text generator.
    Because all AI tools implement an AI tool types, this class is indirectly inherited by all AI tools.

    This class is similar to the AIModelTool interface which is also indirectly inherited by all AI tools.
    This creates a situation where every class that indirectly inherits 1 of the 2 interfaces,
    it also indirectly inherits the other. This could introduces problems like the diamond problem.

    This also might seem redundant as there are 2 classes that do the same. The difference between these 2
    interfaces is that the subclasses of this class are the types of tools, whereas the subclasses of the
    AIModelTool interface are the different AI models.

    As Attributes and methods declared in either class will be available to all AI tools, it doesn't matter
    where they are declared. Except for direct subclasses, as they only inherit from 1 interface. As such,
    the attributes and methods declared here are here specifically for each AI tool type. Likewise,
    the attributes and methods declared in AIModelTool are specifically for each AI model tool.
    """
    def __init__(self) -> None:
        self.tool_name = None

    def call_ai_tool(self, prompt):
        """
        Makes a call to the AI tool
        """
        pass
