import os
from openai import OpenAI

# List of allowed file extensions
ALLOWED_EXTENSIONS = {"c", "cpp", "css", "csv", "docx", "gif", "html", "java", "jpeg", "jpg", "js", "json", "md", "pdf", 
                      "php", "png", "pptx", "py", "rb", "tar", "tex", "ts", "txt", "webp", "xlsx", "xml", "zip"}

def has_allowed_extension(file_name):
    """
    Check if the file has one of the allowed extensions.

    Parameters:
    - file_name (str): The name of the file.

    Returns:
    - bool: True if the file has an allowed extension, False otherwise.
    """
    return file_name.split('.')[-1] in ALLOWED_EXTENSIONS

def list_files_in_folder(folder_path):
    """
    List the names of each file in the given folder and its subfolders,
    including only files with specific extensions.

    Parameters:
    - folder_path (str): The path to the folder.

    Returns:
    - List[str]: A list of file names in the folder and its subfolders.
    """
    all_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if has_allowed_extension(file):
                full_path = os.path.join(root, file)
                all_files.append(full_path)

    return all_files

def read_file_with_fake_content_if_empty(file_path):
    """
    Read a file and return its content. If the file is empty, return fake content.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - str: The content of the file or fake content if the file is empty.
    """
    if os.path.getsize(file_path) == 0:
        return "# This is a placeholder for an empty file\n"
    with open(file_path, 'r') as file:
        return file.read()


# Create a vector store called "Rules"

# Ready the files for upload to OpenAI
folder_name = "src/RobotFrameworkAI/"
file_paths = list_files_in_folder(folder_name)
print(file_paths)
# file_paths = []

print('\n'.join(file_paths))
file_streams = [(path, read_file_with_fake_content_if_empty(path)) for path in file_paths]
f = open("results.txt", "a")
print(file_streams)
# for x in file_streams:
for x in file_streams:
    f.write("\n".join(x))
    f.write("\n\n\n")

# Upload files to the vector store
client = OpenAI(api_key=os.environ["OPENAI_KEY"])
if file_streams:
    vector_store = client.beta.vector_stores.create(name="Rules")
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=[(path, content.encode('utf-8')) for path, content in file_streams]
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)

assistant = client.beta.assistants.create(
    name="ass",
    instructions="""You are a plantuml fanboy and generate class diagram code for plantuml.
    By looking at the contents of the files and the relation in the classes you can create a full fledged class diagram.
    Make sure that all attributes and methods are properly noted. Also some classes inherit other, make sure that is clear in the diagram.
    Make sure each and every method is showing in the diagram even if it is a simple setters. Also make sure each attribute is shown.
    Nothing from the code can be missing everything must be covered every class, attribute method and function should be present aswell as inheritance of classes""",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
client = OpenAI(api_key=os.environ["OPENAI_KEY"])
) if file_streams else client.beta.assistants.create(
    name="ass",
    instructions="""You are a plantuml fanboy and generate class diagram code for plantuml.
    By looking at the contents of the files and the relation in the classes you can create a full fledged class diagram.
    Make sure that all attributes and methods are properly noted. Also some classes inherit other, make sure that is clear in the diagram.
    Make sure each and every method is showing in the diagram even if it is a simple setters. Also make sure each attribute is shown.
    Nothing from the code can be missing everything must be covered every class, attribute method and function should be present aswell as inheritance of classes""",
    model="gpt-3.5-turbo",
)
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": f"File paths: {file_paths}",
        },
        {
            "role": "user",
            "content": "Create the code to generate a class diagram in plantuml.",
        },
    ]
)
# assistant = client.beta.assistants.update(
#     assistant_id=assistant.id,
#     tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
# )
# # The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)

# Use the create and poll SDK helper to create a run and poll the status of
# the run until it's in a terminal state.

# run = client.beta.threads.runs.create_and_poll(
#     thread_id=thread.id, assistant_id=assistant.id
# )

# messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# message_content = messages[0].content[0].text
# annotations = message_content.annotations
# citations = []
# for index, annotation in enumerate(annotations):
#     message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
#     if file_citation := getattr(annotation, "file_citation", None):
#         cited_file = client.files.retrieve(file_citation.file_id)
#         citations.append(f"[{index}] {cited_file.filename}")
# print("\n".join(citations))
# f.write(message_content.value)
# f.write("\n".join(citations))
# print(message_content)
