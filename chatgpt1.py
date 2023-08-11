import os
import json

def load_conversations_from_file(file_path):
    """Load the conversations from the provided file path."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_conversations_to_files(conversations, directory):
    """Save each formatted conversation to a separate .txt file."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    for idx, conversation in enumerate(conversations):
        formatted_conversation = format_conversation(conversation)
        file_path = os.path.join(directory, f"conversation_{idx}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_conversation)
def extract_messages_from_mapping(mapping):
    """Extract messages from the mapping and return them in the order of conversation."""
    messages = []
    for key, value in mapping.items():
        if value['message'] and 'content' in value['message'] and value['message']['content']['content_type'] == 'text':
            messages.append(value['message'])
    # Sort messages based on create_time
    messages.sort(key=lambda x: x['create_time'])
    return messages

def format_conversation(conversation):
    """Format the conversation to a readable text."""
    messages = extract_messages_from_mapping(conversation['mapping'])
    formatted_text = f"Title: {conversation['title']}\n\n"
    for message in messages:
        author = message['author']['role']
        content = " ".join(message['content']['parts'])
        formatted_text += f"{author.capitalize()}: {content}\n\n"
    return formatted_text
# Load the conversations from the file 'conversations.json'
conversations = load_conversations_from_file('conversations.json')

# Determine the directory where the script is being run
script_directory = os.path.dirname(os.path.abspath(__file__))

# Save the conversations to separate .txt files in a directory named 'formatted_conversations'
save_conversations_to_files(conversations, os.path.join(script_directory, "formatted_conversations"))
