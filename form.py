from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# In-memory storage for user responses and classification
tmp=["zombie", "half-zombie", "human"]

responses = []
# CHANGE THIS TO THE AI THINGY THING LATER
user_classification = random.choice (tmp)

beta_database = [
    {"username": "user1", "answers": ['A', 'B', 'C', 'A', 'B'], "classification": "zombie"},
    {"username": "user2", "answers": ['B', 'A', 'C', 'B', 'C'], "classification": "half-zombie"},
    {"username": "user3", "answers": ['C', 'C', 'B', 'A', 'A'], "classification": "human"},
    {"username": "user4", "answers": ['A', 'C', 'A', 'C', 'B'], "classification": "zombie"},
    {"username": "user5", "answers": ['B', 'B', 'C', 'B', 'A'], "classification": "half-zombie"},
    {"username": "user6", "answers": ['C', 'A', 'B', 'C', 'C'], "classification": "human"},
    {"username": "user7", "answers": ['A', 'A', 'A', 'B', 'C'], "classification": "zombie"},
    {"Anvi": "user8", "answers": ['A', 'B', 'A', 'B', 'B'], "classification": "zombie"},
    {"Breanna": "user9", "answers": ['B', 'C', 'C', 'A', 'A'], "classification": "half-zombie"},
    {"Ruqayah": "user10", "answers": ['B', 'C', 'B', 'A', 'A'], "classification": "human"},
    {"username": "user11", "answers": ['B', 'A', 'B', 'C', 'C'], "classification": "half-zombie"},
    {"username": "user12", "answers": ['C', 'C', 'A', 'B', 'A'], "classification": "human"},
    {"username": "user13", "answers": ['A', 'B', 'C', 'C', 'B'], "classification": "zombie"},
    {"username": "user14", "answers": ['B', 'C', 'A', 'B', 'A'], "classification": "half-zombie"},
    {"username": "user15", "answers": ['C', 'A', 'B', 'A', 'C'], "classification": "human"},
    {"username": "user16", "answers": ['A', 'C', 'C', 'B', 'A'], "classification": "zombie"},
    {"username": "user17", "answers": ['B', 'B', 'A', 'C', 'C'], "classification": "half-zombie"},
    {"username": "user18", "answers": ['C', 'C', 'B', 'A', 'B'], "classification": "human"},
    {"username": "user19", "answers": ['A', 'A', 'C', 'C', 'A'], "classification": "zombie"},
    {"username": "user20", "answers": ['B', 'C', 'B', 'B', 'C'], "classification": "half-zombie"},
    {"username": "user21", "answers": ['C', 'A', 'A', 'B', 'B'], "classification": "human"},
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
