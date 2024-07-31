class AIModelTool:
    """
    Interface for all tool models

    This class defines the common methods and attributes that all AI model tools must implement.
    AI model tools are tools for a specific AI model, such as OpenAITools.
    Because all AI tools implement an AI model tools, this class is indirectly inherited by all AI tools.

    This class is similar to the AIToolType interface which is also indirectly inherited by all AI tools.
    This creates a situation where every class that indirectly inherits 1 of the 2 interfaces,
    it also indirectly inherits the other. This could introduces problems like the diamond problem.

    This also might seem redundant as there are 2 classes that do the same. The difference between these 2
    interfaces is that the subclasses of this class are the different AI models, whereas the subclasses of the
    AIToolType interface are the types of tools.

    As Attributes and methods declared in either class will be available to all AI tools, it doesn't matter
    where they are declared. Except for direct subclasses, as they only inherit from 1 interface. As such,
    the attributes and methods declared here are here specifically for each AI model tool. Likewise,
    the attributes and methods declared in AIModelTool are specifically for each AI tool type.
    """
    def __init__(self) -> None:
        self.ai_model_name: str = None
        self.client: object = None
        self.models: list[str] = None
        self.default_model: str = None