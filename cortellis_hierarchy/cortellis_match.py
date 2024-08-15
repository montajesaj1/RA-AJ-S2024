import pandas as pd
import numpy as np
import json
from openai import OpenAI

# Constants

AGGREGATES = {
    "Andrology": "1",
    "Cardiovascular disease": "2",
    "Degeneration": "3",
    "Dermatological disease": "4",
    "Endocrine disease": "5",
    "Fatigue": "6",
    "Gastrointestinal disease": "7",
    "Genetic disorder": "8",
    "Genitourinary disease": "9",
    "Growth disorder": "10",
    "Gynecology and obstetrics": "11",
    "Hematological disease": "12",
    "Immune disorder": "13",
    "Infectious disease": "14",
    "Inflammatory disease": "15",
    "Injury": "16",
    "Metabolic disorder": "17",
    "Mouth disease": "18",
    "Musculoskeletal disease": "19",
    "Neoplasm": "20",
    "Neurological disease": "21",
    "Nutritional disorder": "22",
    "Ocular disease": "23",
    "Otorhinolaryngological disease": "24",
    "Prophylaxis": "25",
    "Psychiatric disorder": "26",
    "Rare disease": "27",
    "Respiratory disease": "28",
    "Surgical procedure": "29",
    "Temperature disorder": "30",
    "Toxicity and intoxication": "31",
    "Ulcer": "32",
    "Unidentified indication": "33"
}

# Step 1. Ingest inxight conditions data and clean it

inxight = pd.read_csv('inxight_to_match.csv')
conditions_arr = inxight['conditions'].to_list()

def split_and_clean(data):
    return [str(d).split('; ') for d in data if not pd.isna(d)]

conditions_arr = split_and_clean(conditions_arr)

# conditions_arr = ['Heart Attack', 'Eczema', 'Flu', 'Diabetes', 'Testicular Cancer']

# Step 2. OpenAI Prompt for 'top 3' aggregate conditions

def classify(inxight):

    client = OpenAI(
        api_key="sk-proj-ma7mp7P30eZmz92lg7lYT3BlbkFJt28LUFIfOw4ByWvi5d0x"
    )

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Which 1-3 terms of {[*AGGREGATES]} best describe {inxight}? Return this as a comma seperated list using the exact names I've provided."}],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content).strip()


def gen_matches(data, inxight):
    
    # prompt = f"You are an expert and medical conditions. Return all the values in {data} which refer to the exact same condition as {inxight} as a comma seperated list"
    prompt = (
        f"You are an expert in medical conditions. "
        f"Return all the values in {data} that refer to the exact same condition as '{inxight}'. "
        f"Only include conditions that are exact synonyms or refer to the same medical condition. "
        f"Provide the response as a comma-separated list using the exact names provided in the list."
        f"An example structure could be: Xerosis, Atopic dermatitis, Eczema, Contact dermatitis"
        f"If there are no matches return None"
    )

    client = OpenAI(
        api_key="sk-proj-ma7mp7P30eZmz92lg7lYT3BlbkFJt28LUFIfOw4ByWvi5d0x"
    )
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content).strip()

import re

def extract_number(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    return None

def match():

    output_list = []
    aggregate_list = []

    for conditions in conditions_arr:
        row = []
        agg_row = []
        
        for condition in conditions:
            condition_matches = []
            agg_matches = []
            if condition:
                disease_list = classify(condition).split(", ")
                key_list = list(map(AGGREGATES.get, disease_list))
                key_list = [int(i) for i in key_list if i is not None]
                paths = [f"data/json/output_pair_{i}.json" for i in key_list]

                print(f'{condition}: {paths}')

                for path in paths:
                    with open(path, 'r') as file:
                        current = json.load(file)
                        matches = gen_matches(current, condition)
                        print(f"matches: {matches}")
                        condition_matches.append(matches.split(', '))
                        keys = list(AGGREGATES.keys())
                        agg_matches.append(keys[extract_number(path) - 1])

                row.append(condition_matches)
                agg_row.append(agg_matches)

            else:
                row.append('None')
                agg_row.append('None')


        output_list.append(row)
        aggregate_list.append(agg_row)

    return output_list, aggregate_list

sample = inxight
sample['Cortellis Matches'], sample['Aggregates'] = match()
print(sample.head())
sample.to_csv('sample.csv')

# if __name__=="__main__":
#     main()
