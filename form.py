from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# In-memory storage for user responses and classification
tmp=["zombie", "half-zombie", "human"]

responses = []
# CHANGE THIS TO THE AI THINGY THING LATER
user_classification = random.choice (tmp)

beta_database = [
    {"username": "Savina", "answers": ['B', 'A', 'A', 'A', 'A'], "classification": "half-zombie"},
    {"username": "Tony", "answers": ['B', 'A', 'B', 'B', 'C'], "classification": "zombie"},
    {"username": "Nikhil", "answers": ['B', 'B', 'C', 'A', 'A'], "classification": "human"},
    {"username": "Ryan", "answers": ['B', 'C', 'B', 'C', 'C'], "classification": "half-zombie"},
    {"username": "Riya", "answers": ['A', 'C', 'A', 'B', 'B'], "classification": "human"},
    {"username": "Anya", "answers": ['B', 'A', 'A', 'A', 'C'], "classification": "human"},
    {"username": "Sukhmani", "answers": ['A', 'A', 'B', 'B', 'B'], "classification": "zombie"},
    {"username": "Anvi", "answers": ['A', 'B', 'A', 'B', 'B'], "classification": "zombie"},
    {"username": "Breanna", "answers": ['B', 'C', 'C', 'A', 'A'], "classification": "half-zombie"},
    {"username": "Ruqayah", "answers": ['B', 'C', 'B', 'A', 'A'], "classification": "half-zombie"},
]


# Define the questions and options
questions = [
    {"question": "Do you prefer brains well done, medium rare, or rare?", "options": ["Well Done", "Medium Rare", "Rare"]},
    {"question": "Do humans taste better in the morning, noon, or at night?", "options": ["Morning", "Noon", "Night"]},
    {"question": "What virus would you use to infect humans? Computer virus, coronavirus, or zombie virus?", "options": ["Computer virus", "Coronavirus", "Zombie virus"]},
    {"question": "Do you prefer to bite humans in the neck, arm, or foot?", "options": ["Neck", "Arm", "Foot"]},
    {"question": "What is your superpower?", "options": ["Agility", "Night Vision", "Fear Aura"]}
]

# Mapping from option index to letter
option_map = ['A', 'B', 'C']

def classify_user():
    global user_classification
    user_classification = random.choice(["zombie", "half-zombie", "human"])
    return user_classification

def find_best_match(user_responses):
    best_match = None
    highest_similarity = -1

    for user in beta_database:
        if user["classification"] == user_classification:
            similarity = sum(1 for a, b in zip(user["answers"], user_responses) if a == b)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = user

    return best_match

@app.route('/')
def home():
    print(responses)
    if len(responses) < len(questions):
        current_question = questions[len(responses)]
        return render_template('index.html', question=current_question["question"], options=current_question["options"], responses=responses)
    else:
        if user_classification is None:
            classify_user()
        best_match = find_best_match(responses)
        return render_template('result.html', classification=user_classification, best_match=best_match)
        return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/submit', methods=['POST'])
def submit():
    response = request.form.get('response')
    if response:
        question_index = len(responses)
        option_index = questions[question_index]["options"].index(response)
        mapped_response = option_map[option_index]
        responses.append(mapped_response)
    return redirect(url_for('home'))

@app.route('/back')
def back():
    if responses:
        responses.pop()
    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    global responses, user_classification
    responses = []
    user_classification = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
