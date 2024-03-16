import json
import string
from difflib import get_close_matches

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def preprocess_text(text: str) -> str:
    # Convert text to lowercase and remove punctuation
    processed_text = text.lower()
    processed_text = processed_text.translate(str.maketrans('', '', string.punctuation))
    return processed_text

def find_best_match(user_question: str, questions: list[str]):
    # Preprocess user question and questions in knowledge base
    user_question_processed = preprocess_text(user_question)
    questions_processed = [preprocess_text(question) for question in questions]

    # Compute bag-of-words representations
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([user_question_processed] + questions_processed)

    # Compute cosine similarity between user question and knowledge base questions
    similarity_scores = cosine_similarity(X)[0][1:]

    # Find the index of the question with the highest similarity score
    best_match_index = similarity_scores.argmax()

    # Return the best matching question or None if no match
    if similarity_scores[best_match_index] > 0:
        return questions[best_match_index]
    else:
        return None

def get_answer_for_question(question: str, knowledge_base: dict):
    for q in knowledge_base["questions"]:
        if q['question'] == question:
            return q["answer"]
    return None  # If no answer found for the question

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('You: ')

        if user_input == 'quit':
            break

        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank You! I learned a new response!')

if __name__ == '__main__':
    chat_bot()