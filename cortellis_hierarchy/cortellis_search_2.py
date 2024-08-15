import json
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
        messages=[{"role": "user", "content": f"You are an expert and medical conditions. Return 'yes' if these two terms mean the exact same thing, 'no' otherwise: {cortellis}, {inxight}"}],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content).strip()

def find_all_paths_to_node(node, target_string, current_path=None):
    if current_path is None:
        current_path = []
    
    matches = set()

    for key in node:
        new_path = current_path + [key]
        
        # Check if the current key matches the target string
        if key.lower() == target_string.lower() or target_string.lower() in key.lower().split():
            matches.add(tuple(new_path))
        
        # Check if the response function returns 'yes' for the current key and target string
        if response(key, target_string).lower() == 'yes':
            matches.add(tuple(new_path))

        # If the current value is a dictionary, recursively search
        if isinstance(node[key], dict):
            matches.update(find_all_paths_to_node(node[key], target_string, new_path))
    
    return matches

# Example usage
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
#             }
#         }
#     }
# }
#
# # Example usage:
# target_nodes = ["Prostatitis", "Orchitis", "Epididymitis", "Balanitis", "Acute bacterial prostatitis"]
#
# def search(data, target_node):
#     paths = find_all_paths_to_node(data, target_node)
#     if paths:
#         for path in paths:
#             print(f"Path to '{target_node}': {' -> '.join(path)}")
#     else:
#         print(f"No path found to '{target_node}'.")
#
# for node in target_nodes:
#     search(andrology_data, node)
