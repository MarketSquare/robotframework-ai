class AIModelStrategy:
    """
    The interface class for AI model strategies.
    A prompt can be handled by different AI models.
    Each AI model can be used as a strategy to perform the task of responding to the prompt.

    To add a new AI model, create a new class in this folder and have it inherit this interface.
    Create the logic for unpacking a Prompt object, sending it to the AI model and pack its 
    response in a Response object.

    Make sure the send_prompt method is implemented to accept the Prompt and return the Response.
    Adding an object of this class to the ai_models in the AI_Interface class will allow you to
    to use that AI model for the generation of data.
    """
    def __init__(self) -> None:
        self.ai_model = None

    def send_prompt(self, prompt):
        pass