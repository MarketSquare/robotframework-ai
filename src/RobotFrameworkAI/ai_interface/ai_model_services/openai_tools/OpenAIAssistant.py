from openai import OpenAI
from RobotFrameworkAI.ai_interface.ai_model_services.openai_tools.OpenAITool import OpenAITool
from RobotFrameworkAI.ai_interface.ai_model_tools.AssistantTool import AssistantTool
from RobotFrameworkAI.objects.response.Response import Response
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata
import logging

logger = logging.getLogger(__name__)

class OpenAIAssistant(OpenAITool, AssistantTool):
    """
    The AI tool in charge of handling all assistant actions for OpenAI

    Implements all abstract method for handling actions with the OpenAI assistant.
    """
    def __init__(self, client) -> None:
        print(__name__)
        OpenAITool.__init__(self)
        AssistantTool.__init__(self)
        self.client:OpenAI = client

    # Actions
    def create_assistant(self, prompt):
        assistant_data = prompt.ai_tool_data

        model = self.default_model if prompt.config.model is None else prompt.config.model

        self.assistant = self.client.beta.assistants.create(
            name = assistant_data.name,
            model = model,
            instructions = assistant_data.instructions,
            tools = [{"type": "file_search"}],
            temperature = prompt.parameters["temperature"],
            top_p = prompt.parameters["top_p"],
            response_format = prompt.config.response_format
        )
        self.create_new_thread()
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, model)
        response = Response(self.assistant.id, response_metadata)
        return response

    def update_assistant(self, prompt):
        assistant_data = prompt.ai_tool_data

        model = self.default_model if prompt.config.model is None else prompt.config.model
        updated_parameters = [
            f"Name from `{assistant_data.name}` to `{self.assistant.name}`" if assistant_data.name != self.assistant.name else "",
            f"Model from `{self.assistant.model}` to `{model}`" if model != self.assistant.model else "",
            f"Instructions from `{assistant_data.instructions}` to `{self.assistant.instructions}`" if assistant_data.instructions != self.assistant.instructions else "",
            f"Temperature from `{self.assistant.temperature}` to `{prompt.parameters['temperature']}`" if prompt.parameters['temperature'] != self.assistant.temperature else "",
            f"Top_p from `{self.assistant.top_p}` to `{prompt.parameters['top_p']}`" if prompt.parameters['top_p'] != self.assistant.top_p else "",
            f"Response_format from `{self.assistant.response_format}` to `{prompt.config.response_format}`" if prompt.config.response_format != self.assistant.response_format else ""
        ]
        # Remove empty strings from list
        updated_parameters = [updated_parameter for updated_parameter in updated_parameters if updated_parameter]
        
        updated_parameters = updated_parameters if updated_parameters else ["no parameters have been updated."]        
        message = f"Successfully updated assistant `{self.assistant.name}` with id `{self.assistant.id}`. Updated parameters: {', '.join(updated_parameters)}."
        
        self.assistant = self.client.beta.assistants.update(
            self.assistant.id,
            name=assistant_data.name,
            model=model,
            instructions=assistant_data.instructions,
            tools=[{"type": "file_search"}],
            temperature=prompt.parameters["temperature"],
            top_p=prompt.parameters["top_p"],
            response_format=prompt.config.response_format
        )
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, model)
        response = Response(message, response_metadata)
        return response


    def get_active_assistant_id(self, _ = None):
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        response = Response(self.assistant.id, response_metadata)
        return response

    def delete_assistant(self, _ = None):
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        response = Response(self.client.beta.assistants.delete(self.assistant.id), response_metadata)
        self.assistant = None
        return response

    def delete_assistant_by_id(self, prompt):
        id = prompt.ai_tool_data.id
        if id == self.assistant.id:
            self.assistant = None
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        response = Response(self.client.beta.assistants.delete(id), response_metadata)
        return response

    def set_active_assistant(self, prompt):
        id = prompt.ai_tool_data.id
        previous_active_assistant = self.assistant
        self.assistant = self.get_assistant(id)
        self.create_new_thread()
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        message = f"Succesfully set assistant `{self.assistant.name}` with id `{self.assistant.id}` as the active assistant. Previous active assistant: name: `{previous_active_assistant.name}`, id: `{previous_active_assistant.id}`"
        response = Response(message, response_metadata)
        return response 

    def attach_files(self, prompt):
        file_paths = prompt.ai_tool_data.file_paths
        files = self.prepare_files(file_paths)
        vector_store = self.client.beta.vector_stores.create()
        self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[(path, content.encode('utf-8')) for path, content in files]
        )
        self.assistant = self.client.beta.assistants.update(
            assistant_id = self.assistant.id,
            tool_resources = {"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        message = f"Succesfully added {len(files)} files to assistant with id `{self.assistant.id}` and name `{self.assistant.name}`. The following files got added: `{'`, `'.join([file[0] for file in files])}`"
        response = Response(message, response_metadata)
        return response

    def send_message(self, prompt):
        self.add_message_to_thread(prompt.message, prompt.ai_tool_data.file_paths)
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id = self.thread.id, assistant_id = self.assistant.id
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id, run_id=run.id))
        message = messages[0]
        message_content = message.content[0].text.value
        model = self.default_model if prompt.config.model is None else prompt.config.model
        token_usage = run.usage
        # Finish reason is not available with OpenAI assistants, so for now it's set to None
        response_metadata = ResponseMetadata(
            self.tool_name, self.ai_model_name, model, None, token_usage.prompt_tokens, token_usage.completion_tokens, message.created_at
        )
        response = Response(message_content, response_metadata)
        return response

    def create_new_thread(self, _ = None):        
        self.thread = self.client.beta.threads.create()
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        message = f"Succesfully created new thread with id `{self.thread}` for assistant `{self.assistant.name}` with id `{self.assistant.id}`"
        response = Response(message, response_metadata)
        return response
    
    def set_active_assistant(self, prompt):
        id = prompt.ai_tool_data.id
        previous_assistant = self.assistant
        self.assistant = self.get_assistant(id)
        self.create_new_thread()
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, self.assistant.model)
        message = f"Succesfully changed the active assistant to assistant `{self.assistant.name}` with id `{self.assistant.id}` from assistant `{previous_assistant.name}` with id `{previous_assistant.id}`"
        response = Response(message, response_metadata)
        return response

    # Helper functions
    def get_assistant(self, id):
        return self.client.beta.assistants.retrieve(id)

    def upload_file(self, file):
        file = self.client.files.create(
            file = file,
            purpose = 'assistants'
            )
        return file.id

    def add_message_to_thread(self, message, file_paths=None):
        if file_paths:
            files = self.prepare_files(file_paths)
            file_ids = [self.upload_file(file) for file in files]
            return self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message.user,
                attachments=[{
                    "file_id": file_id,
                    "tools": [{"type": "file_search"}]
                } for file_id in file_ids][:10]
            )
        else:
            return self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message.user
            )
