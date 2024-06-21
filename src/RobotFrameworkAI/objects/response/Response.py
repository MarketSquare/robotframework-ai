from dataclasses import dataclass
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata

@dataclass
class Response:
    """
    The object that holds all information needed from a response from an AI model.

    Response objects are used as a standardized way of communication between modules and AI models.
    Each AIModelStrategy creates a Response and sends it to the AI_Interface. The AI_Interface will then send it
    back to the appropriate module, which in turn unpacks this object and sends the data to the user.

    A Response contains a message with the response of the AI model.
    The metadata is an object that contains information about the Response itself, which can be used for logging.
    """
    message: str
    metadata: ResponseMetadata
