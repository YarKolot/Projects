import json
import os

def load_training_data(folder_path):
    training_file = os.path.join(folder_path, 'training.json')
    if os.path.exists(training_file):
        with open(training_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_new_training(user_input, bot_response, folder_path):
    training_file = os.path.join(folder_path, 'training.json')
    
    if not os.path.exists(training_file):
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)

    with open(training_file, 'r', encoding='utf-8') as f:
        training_data = json.load(f)

    for category, phrases in training_data.items():
        if user_input in phrases:
            if isinstance(phrases[user_input], list):
                phrases[user_input].append(bot_response)
            else:
                phrases[user_input] = [phrases[user_input], bot_response]
            break
    else:
        training_count = len(training_data) + 1
        new_training = {f"training{training_count}": {user_input: [bot_response]}}
        training_data.update(new_training)

    with open(training_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)

def check_if_phrase_exists(user_input, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for category, phrases in data.items():
                    if user_input in phrases:
                        return True, category, phrases[user_input]
    return False, None, None

def main():
    folder_path = 'responses'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print("Интерактивный тренер готов")

    while True:
        user_input = input("Введите фразу юзера: ").strip()
        if user_input.lower() == "exit":
            break

        exists, category, responses = check_if_phrase_exists(user_input, folder_path)
        
        if exists:
            print(f"Фраза уже существует в базе, текущие ответы: {responses}")
            add_new = input("Хотите добавить ещё один ответ? (y/n): ").strip().lower()
            if add_new == "y":
                bot_response = input("Введите новый ответ бота: ").strip()
                save_new_training(user_input, bot_response, folder_path)
                print(f"Добавлен новый ответ: {user_input} -> {bot_response}")
            else:
                print("Ответ не был добавлен")
        else:
            bot_response = input("Введите ответ бота: ").strip()
            save_new_training(user_input, bot_response, folder_path)
            print(f"Тренер-бот сохранил: {user_input} -> {bot_response}")

if __name__ == "__main__":
    main()