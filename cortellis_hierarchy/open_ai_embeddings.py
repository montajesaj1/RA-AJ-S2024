import openai
import numpy as np
from scipy.spatial.distance import cosine

from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))

# df.to_csv('output/embedded_1k_reviews.csv', index=False)

# def get_embedding(text):
#     response = openai.Embedding.create(
#         input=[text],
#         model="text-embedding-ada-002"
#     )
#     return response['data'][0]['embedding']

def cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

import pytest

SIMILARITY_THRESHOLD = 0.10

def is_similar(term1, term2):
    embedding1 = get_embedding(term1)
    embedding2 = get_embedding(term2)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity >= SIMILARITY_THRESHOLD

@pytest.mark.parametrize("term1, term2, expected", [
    ("Atopic Dermatitis", "Eczema", True),
    ("Cardiac failure", "heart failure", True),
    ("Thrombosis", "Venous Thromboembolism", True),
    ("Depression", "Depressive disorder", True),
    ("Basal cell carcinoma", "Non-melanoma skin cancer", True),
    ("Osteoarthritis", "Osteoarthrosis", True),
    ("Hypertension", "High blood pressure", True),
    ("Myocardial infarction", "Heart attack", True),
    ("Cerebrovascular accident", "Stroke", True),
    ("Type 2 Diabetes Mellitus", "Type 2 Diabetes", True),
    ("Epilepsy", "Seizure disorder", True),
    ("Hyperlipidemia", "High cholesterol", True),
    ("Chronic Obstructive Pulmonary Disease", "COPD", True),
    ("Asthma", "Chronic respiratory disease", True),
    ("Gastroesophageal reflux disease", "GERD", True),
    ("Hepatitis C", "HCV infection", True),
    ("Influenza", "Flu", True),
    ("Rheumatoid arthritis", "RA", True),
    ("Schizophrenia", "Psychotic disorder", True),
    ("Systemic lupus erythematosus", "Lupus", True),
    ("Tuberculosis", "TB", True),
    ("Varicella", "Chickenpox", True),
    ("Vitiligo", "Skin depigmentation disorder", True),
    ("Zoster", "Shingles", True),
    ("Cholelithiasis", "Gallstones", True),
    ("Pancreatitis", "Pancreas inflammation", True),
    ("Osteoporosis", "Bone density loss", True),
    ("Psoriasis", "Chronic skin condition", True),
    ("Leukemia", "Blood cancer", True),
    ("Malignant melanoma", "Skin cancer", True),
    ("Anxiety disorder", "Generalized anxiety disorder", True),
    ("Hypertension", "Diabetes", False),
    ("Myocardial infarction", "Stroke", False),
    ("Cerebrovascular accident", "Asthma", False),
    ("Type 2 Diabetes Mellitus", "Hepatitis C", False),
    ("Epilepsy", "COPD", False),
    ("Hyperlipidemia", "Psoriasis", False),
    ("Chronic Obstructive Pulmonary Disease", "Osteoporosis", False),
    ("Asthma", "Schizophrenia", False),
    ("Gastroesophageal reflux disease", "Tuberculosis", False),
    ("Hepatitis C", "Vitiligo", False),
    ("Influenza", "Leukemia", False),
    ("Rheumatoid arthritis", "Zoster", False),
    ("Schizophrenia", "Pancreatitis", False),
    ("Systemic lupus erythematosus", "Cholelithiasis", False),
    ("Tuberculosis", "Anxiety disorder", False),
    ("Varicella", "Depression", False),
    ("Vitiligo", "Basal cell carcinoma", False),
    ("Zoster", "Thrombosis", False),
    ("Cholelithiasis", "Hypertension", False),
    ("Pancreatitis", "Myocardial infarction", False),
    ("Osteoporosis", "Cerebrovascular accident", False),
    ("Psoriasis", "Type 2 Diabetes Mellitus", False),
    ("Leukemia", "Epilepsy", False),
    ("Malignant melanoma", "Hyperlipidemia", False),
    ("Anxiety disorder", "Chronic Obstructive Pulmonary Disease", False),
    ("Epididymitis", "Epididymo-orchitis", True),
    ("Orchitis", "Epididymo-orchitis", True),
    ("Orchitis", "Periorchitis", True),
    ("Prostate tumor", "Hormone dependent prostate cancer", True),
    ("Prostate tumor", "Hormone refractory prostate cancer", True),
    ("Prostate tumor", "Metastatic prostate cancer", True),
    ("Prostate tumor", "Prostatic intraepithelial neoplasia", True),
    ("Testis tumor", "Metastatic testicular cancer", True),
    ("Testis tumor", "Seminoma", True),
    ("Balanitis", "Penis disease", False),
    ("Prostatitis", "Prostate hyperplasia", False),
    ("Cryptorchidism", "Orchialgia", False),
    ("Aspermia", "Teratospermia", False),
    ("Azoospermia", "Oligospermia", False),
    ("Male genital system disease", "Male infertility", False),
    ("Male genital tract tumor", "Male breast neoplasm", False),
    ("Male sexual dysfunction", "Prostate disease", False),
    ("Microphallus", "Penis injury", False),
    ("Phimosis", "Priapism", False),
    ("Globozoospermia", "Asthenozoospermia", False)
])

def test_similarity(term1, term2, expected):
    assert is_similar(term1, term2) == expected, f"For {term1} and {term2}, expected {expected} but got {not expected}"

if __name__ == "__main__":
    pytest.main()
