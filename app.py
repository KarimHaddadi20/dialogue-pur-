
from difflib import get_close_matches
from fuzzywuzzy import process

from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_knowledge_base(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_knowledge_base(filename, knowledge_base):
    with open(filename, 'w') as file:
        json.dump(knowledge_base, file)

def find_best_match(user_input, questions):
    for question in questions:
        if user_input in question:
            return question
    return None

def find_best_match(user_input, questions):
    # Utiliser fuzzywuzzy pour trouver la question la plus proche
    best_match = process.extractOne(user_input, questions)
    # best_match est un tuple où le premier élément est la meilleure correspondance
    # et le deuxième élément est le score de correspondance
    if best_match[1] > 80:  # Vous pouvez ajuster ce seuil en fonction de vos besoins
        return best_match[0]
    return None

def get_anwser_for_question(match, knowledge_base):
    # Parcourir chaque question dans la base de connaissances
    for item in knowledge_base["questions"]:
            # Si la question correspond à la question trouvée
        if item["question"] == match:
            return item["answer"]
    return None


# Définir la route principale de l'application

@app.route('/', methods=['GET', 'POST'])
def chat_bot():
    user_input = ""
    response = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        knowledge_base = load_knowledge_base("knowledge_base.json")

        matches = find_best_match(user_input, [question["question"] for question in knowledge_base["questions"]])

        if matches:
            response = get_anwser_for_question(matches, knowledge_base)
        else:
            response = "J'ai pas compris votre question, pouvez-vous reformuler ?"
            new_answer: str = request.form.get('new_answer')

            if new_answer is not None and new_answer.lower() != "adi":
                if "questions" not in knowledge_base:
                    knowledge_base["questions"] = []
                knowledge_base["questions"].append({"question": user_input , "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                response = "bot: j'ai bien compris ce que t'a dis  !"

    return render_template('chat.html', response=response)

if __name__ == "__main__":
    app.run(debug=True)

    


