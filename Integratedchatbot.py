from flask import Flask, render_template, request, jsonify
import json
import string
from difflib import get_close_matches
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load knowledge base from JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Save knowledge base to JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Preprocess text (convert to lowercase and remove punctuation)
def preprocess_text(text: str) -> str:
    processed_text = text.lower()
    processed_text = processed_text.translate(str.maketrans('', '', string.punctuation))
    return processed_text

# Find the best match for user input in the knowledge base
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

# Get answer for the best matching question
def get_answer_for_question(question: str, knowledge_base: dict):
    for q in knowledge_base["questions"]:
        if q['question'] == question:
            return q["answer"]
    return None

# Route for serving the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    knowledge_base = load_knowledge_base('knowledge_base.json')
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({'speaker': 'Chatbot', 'message': answer})
    else:
        return jsonify({'speaker': 'Chatbot', 'message': 'I don\'t know the answer. Can you teach me?'})

# Route for handling button clicks
@app.route('/button_click', methods=['POST'])
def button_click():
    button_value = request.form['button_value']
    return jsonify({'speaker': 'User', 'message': button_value})

if __name__ == '__main__':
    app.run(debug=True)


