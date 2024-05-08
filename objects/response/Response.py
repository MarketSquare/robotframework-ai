from objects.response.ResponseMetadata import ResponseMetadata


class Response:
    def __init__(self, message:str, metadata:ResponseMetadata) -> None:
        self.message = message
        self.metadata = metadata