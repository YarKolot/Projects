import json
import spacy
import numpy as np
import random
import os
from numpy import dot
from numpy.linalg import norm

nlp = spacy.load("ru_core_news_md")

def vectorize_text(text):
    doc = nlp(text)
    return doc.vector

def cosine_similarity(v1, v2):
    if norm(v1) == 0 or norm(v2) == 0:
        return 0.0
    return dot(v1, v2) / (norm(v1) * norm(v2))

def load_responses_from_folder(folder_path):
    all_responses = {}
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    responses = json.load(f)
                    all_responses.update(responses)
        return all_responses
    except FileNotFoundError:
        print(f"Папка {folder_path} не найдена.")
        return {}

def get_exact_response(user_input, responses):
    for category, phrases in responses.items():
        if user_input in phrases:
            possible_responses = phrases[user_input]
            return random.choice(possible_responses) if isinstance(possible_responses, list) else possible_responses
    return None

def get_best_response(user_input, responses):
    user_vector = vectorize_text(user_input)
    best_response = None
    max_similarity = -1

    for category, phrases in responses.items():
        for question in phrases:
            question_vector = vectorize_text(question)
            similarity = cosine_similarity(user_vector, question_vector)

            if similarity > max_similarity:
                max_similarity = similarity
                possible_responses = phrases[question]
                best_response = random.choice(possible_responses) if isinstance(possible_responses, list) else possible_responses

    return best_response if max_similarity > 0.7 else "Не знаю что ответить"

def main():
    responses = load_responses_from_folder('responses')
    print("Гриша проснулся и готов к эксплоутации")

    while True:
        user_input = input("Юзер: ").strip()
        if user_input.lower() in ["exit", "stop"]:
            print("Гриша: Я спать пошел")
            break

        response = get_exact_response(user_input, responses)
        if response:
            print(f"Гриша: {response}")
        else:
            response = get_best_response(user_input, responses)
            print(f"Гриша: {response}")

if __name__ == "__main__":
    main()