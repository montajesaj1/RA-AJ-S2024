import pandas as pd
import numpy as np
import json
from openai import OpenAI
import ast

data = pd.read_excel('5_cortellis_inxight_simple.xlsx')

def process_row(row):
    try:
        evaluated_row = ast.literal_eval(row)
        if isinstance(evaluated_row, list):
            # Check if it's a list of lists
            if all(isinstance(i, list) for i in evaluated_row):
                return [item for sublist in evaluated_row for item in sublist]
            else:
                return evaluated_row
        else:
            return [evaluated_row]
    except:
        return [row]

data['flattened'] = data['Cortellis Matches'].apply(process_row)

def best_match(curr, matches):

    client = OpenAI(
        api_key="sk-proj-ma7mp7P30eZmz92lg7lYT3BlbkFJt28LUFIfOw4ByWvi5d0x"
    )

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Return the single best match to {curr} from {matches} as a single string, do not include any additional words in your response, if there is no input data return the string None"}],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content).strip()

def main():
    flattened = data['flattened'].to_list()
    inxight = data['Inxight Conditions'].to_list()
    acc = 0
    output = []

    for i in flattened:
        curr = best_match(inxight[acc], i)
        output.append(curr)
        acc += 1

    data['best_match'] = output
    data.to_csv('7_best_match.csv', index=False)

if __name__=="__main__":
    main()
