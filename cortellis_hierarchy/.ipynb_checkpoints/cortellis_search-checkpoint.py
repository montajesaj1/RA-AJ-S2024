import json
import prompt_module as pm
from openai import OpenAI
import re

def response(cortellis, inxight):
    """
    Initializes an OpenAI gpt-3.5 model with generated prompt 

    """

    client = OpenAI(
        api_key="sk-proj-ma7mp7P30eZmz92lg7lYT3BlbkFJt28LUFIfOw4ByWvi5d0x"
    )

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"You are an expert on diseases and medical conditions return yes if these two terms are synonyms, no otherwise: {cortellis}, {inxight}" }],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content)

def find_path_to_node(node, target_string, current_path=[]):
    # Iterate through keys in the current node
    for key in node:
        # Append the current key to the current path
        current_path.append(key)
        
        # Check if the current key matches the target string
        if key.lower() == target_string.lower():
            return current_path

        if target_string.lower() in key.lower().split():
            return current_path

        # elif response(key, target_string) == 'yes':
            # return current_path

        # elif key != target_string:
            # if response(key, target_string) == 'yes':
                # return current_path
        
        # If the current value is a dictionary, recursively search
        if isinstance(node[key], dict):
            found_path = find_path_to_node(node[key], target_string, current_path)
            if found_path is not None:
                return found_path
        
        # Remove the last added key to backtrack
        current_path.pop()
    
    # If no path is found, return None
    return None

# andrology_data = {
#     "Andrology": {
#         "Male contraception": {},
#         "test": {
#             "Hematocele": {},
#             "Male genital tract inflammation": {
#                 "Balanitis": {},
#                 "Epididymitis": {
#                     "Epididymo-orchitis": {}
#                 },
#                 "Orchitis": {
#                     "Epididymo-orchitis": {},
#                     "Periorchitis": {}
#                 },
#                 "Prostatitis": {}
#             },
#             # ... (rest of the structure)
#         },
#         # ... (rest of the structure)
#     }
# }
#

# Convert to JSON if not already in dictionary format
# andrology_data = json.loads(andrology_json_string)

# Example usage:
# target_nodes = ["Prostatitis", "Orchitis", "Epididymitis", "Balanitis", "Acute bacterial prostatitis"]

# def search(data, target_node):
#     path = find_path_to_node(data, target_node)
#     if path is not None:
#         print(f"Path to '{target_node}': {' -> '.join(path)}")
#     else:
#         print(f"No path found to '{target_node}'.")
#
# for node in target_nodes:
#     search(andrology_data, node)

# target_node = "Acute bacterial prostatitis"
# path = find_path_to_node(andrology_data, target_node)
# if path is not None:
#     print(f"Path to '{target_node}': {' -> '.join(path)}")
# else:
#     print(f"No path found to '{target_node}'.")
