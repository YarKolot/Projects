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
    return dot(v1, v2) / (norm(v1) * norm(v2)) if norm(v1) and norm(v2) else 0.0

def load_responses_from_folder(folder_path):
    all_responses = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                responses = json.load(f)
                all_responses.update(responses)
    return all_responses

def save_new_dialog(user_input, bot_response, folder_path):
    dialogs_file = os.path.join(folder_path, 'dialogs.json')
    
    if not os.path.exists(dialogs_file):
        with open(dialogs_file, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

    with open(dialogs_file, 'r', encoding='utf-8') as f:
        dialogs_data = json.load(f)

    dialog_count = len(dialogs_data) + 1
    new_dialog = {f"dialog{dialog_count}": {user_input: [bot_response]}}

    dialogs_data.update(new_dialog)
    
    with open(dialogs_file, 'w', encoding='utf-8') as f:
        json.dump(dialogs_data, f, ensure_ascii=False, indent=4)

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
    folder_path = 'responses'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    responses = load_responses_from_folder(folder_path)
    print("Тренер-бот готов к работе")

    while True:
        user_input = input("Юзер: ").strip()
        if user_input.lower() == "exit":
            break

        response = get_exact_response(user_input, responses)

        if not response:
            response = get_best_response(user_input, responses)
            if response == "Не знаю что ответить":
                response = input("Введите ответ для этого вопроса: ").strip()
                save_new_dialog(user_input, response, folder_path)

        print(f"Тренер-бот: {response}")

if __name__ == "__main__":
    main()
