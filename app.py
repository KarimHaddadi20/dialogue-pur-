import json
from difflib import get_close_matches

# Charger la base de connaissances à partir d'un fichier JSON
def load_knowledge_base(file_path: str) -> dict:
  with open(file_path, 'r') as file:
    data: dict = json.load(file)
  return data

# Sauvegarder la base de connaissances dans un fichier JSON
def save_knowledge_base(file_path: str, data: dict):
  with open(file_path, 'w') as file:
    json.dump(data, file, indent=2)

# Trouver la meilleure correspondance pour une question de l'utilisateur dans la liste des questions connues
def find_best_match(user_question: str, question: list[str]) -> str | None:
  matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
  return matches[0] if matches else None

# Obtenir la réponse à une question de la base de connaissances
def get_anwser_for_question(question: str, knowledge_base: dict) -> str | None:
  for q in knowledge_base["questions"]:
    if q["question"] == question:
      return q["answer"]

# La fonction principale du chatbot
def chat_bot():
  # Charger la base de connaissances
  knowledge_base: dict = load_knowledge_base("knowledge_base.json")

  while True:
    # Obtenir l'entrée de l'utilisateur
    user_input: str = input("you: ")

    # Si l'utilisateur tape "quit", terminer le chat
    if user_input.lower() == "quit":
      break

    # Trouver la meilleure correspondance pour la question de l'utilisateur
    best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        # Si une correspondance a été trouvée, obtenir la réponse et l'imprimer
        answer: str = get_anwser_for_question(best_match, knowledge_base)
        print(f"bot: {answer}")
    else:
        # Si aucune correspondance n'a été trouvée, demander à l'utilisateur la réponse
        print("bot: semhyi ur fhimegh ara tameslayt-ik")
        new_answer: str = input('arud tameslayt-ik negh "adi" iwaken atadid: ')

        # Si la réponse de l'utilisateur n'est pas "adi", ajouter la question et la réponse à la base de connaissances
        if new_answer.lower() != "adi":
          if "questions" not in knowledge_base:
            knowledge_base["questions"] = []
          knowledge_base["questions"].append({"question": user_input , "answer": new_answer})
          save_knowledge_base("knowledge_base.json", knowledge_base)
          print("bot: tanemmirt ik ! asagi talemad lhaja !")

if __name__ == "__main__":
  # Démarrer le chatbot
  chat_bot()
  

