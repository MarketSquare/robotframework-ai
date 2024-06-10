from openai import OpenAI
from RobotFrameworkAI.ai_interface.ai_model_services.openai_tools.OpenAITool import OpenAITool
from RobotFrameworkAI.ai_interface.ai_model_tools.AssistantTool import AssistantTool
from RobotFrameworkAI.objects.response.Response import Response
from RobotFrameworkAI.objects.response.ResponseMetadata import ResponseMetadata


class OpenAIAssistant(OpenAITool, AssistantTool):
    def __init__(self, client) -> None:
        print(__name__)
        OpenAITool.__init__(self)
        AssistantTool.__init__(self)
        self.client:OpenAI = client

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
        response_metadata = ResponseMetadata(self.tool_name, self.ai_model_name, model)
        response = Response(self.assistant.id, response_metadata)
        return response

    def get_active_assistant_id(self):
        return self.assistant.id

    def delete_assistant(self, id):
        return self.client.beta.assistants.delete(id)

    def delete_active_assistant(self):
        return self.client.beta.assistants.delete(self.assistant.id)

    def get_assistant(self, id):
        return self.client.beta.assistants.retrieve(id)
    
    def set_active_assistant(self, id):
        self.assistant = self.get_assistant(id)

    def attach_files_to_assistant(self, files):
        vector_store = self.client.beta.vector_stores.create()
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[(path, content.encode('utf-8')) for path, content in files]
        )
        print(file_batch.file_counts)
        self.assistant = self.client.beta.assistants.update(
            assistant_id = self.assistant.id,
            tool_resources = {"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        response_metadata = ResponseMetadata(
            self.tool_name, self.ai_model_name, None
        )
        response = Response(f"Succesfully added {len(files)} files to assistant with id: {self.assistant.id}. The following files got added: `{"`, `".join([file[0] for file in files])}`", response_metadata)

    def send_prompt_to_assistant(self, prompt):
        thread = self.client.beta.threads.create(
            messages = prompt.message
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id = thread.id, assistant_id = self.assistant.id
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
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
