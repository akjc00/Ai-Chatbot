import json
import string
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def preprocess_text(text: str) -> str:
    processed_text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return processed_text

def find_best_match(user_question: str, questions: list[str]):
    user_question_processed = preprocess_text(user_question)
    questions_processed = [preprocess_text(question) for question in questions]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([user_question_processed] + questions_processed)

    similarity_scores = cosine_similarity(X)[0][1:]
    best_match_index = similarity_scores.argmax()

    if similarity_scores[best_match_index] > 0:
        return questions[best_match_index]
    else:
        return None

def get_answer_for_question(question: str, knowledge_base: dict):
    for q in knowledge_base["questions"]:
        if q['question'] == question:
            return q["answer"]
    return None

def read_internship_database(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        lines = file.readlines()
        entry = {}
        entries = []

        for line in lines:
            line = line.strip()
            if line:
                if line == '-----------------------------------------------------------------------------------------------':
                    if entry:
                        entries.append(entry)
                        entry = {}
                else:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        entry[key.strip()] = value.strip()
                    else:
                        print(f"Ignoring line: {line}. Delimiter ':' not found.")

        if entry:
            entries.append(entry)

    return entries

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    knowledge_base = load_knowledge_base('knowledge_base.json')
    internship_database = read_internship_database('internship_database.txt')

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({'bot_response': answer})
    else:
        for internship in internship_database:
            for key, value in internship.items():
                if key.lower() in user_input.lower() or value.lower() in user_input.lower():
                    return jsonify({'bot_response': value})
        else:
            return jsonify({'bot_response': "I don't know the answer. Can you teach me?"})

if __name__ == '__main__':
    app.run(debug=True)

