from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

responses = []

questions = [
    {
        "question": "Do you prefer brains well done, medium rare, or rare?",
        "options": ["Well Done", "Medium Rare", "Rare"]
    },
    {
        "question": "Do humans taste better in the morning, noon, or at night?",
        "options": ["Morning", "Noon", "Night"]
    },
    {
        "question": "What virus would you use to infect humans? Computer virus, coronavirus, or zombie virus?",
        "options": ["Computer virus", "Coronavirus", "Zombie virus"]
    },
    {
        "question": "Do you prefer to bite humans in the neck, arm, or foot?",
        "options": ["Neck", "Arm", "Foot"]
    },
    {
        "question": "What is your superpower?",
        "options": ["Agility", "Night Vision", "Fear Aura"]
    }
]

@app.route('/')
def home():
    if len(responses) < len(questions):
        current_question = questions[len(responses)]
        return render_template('index.html', question=current_question["question"], options=current_question["options"])
    else:
        return redirect(url_for('loading'))

@app.route('/submit', methods=['POST'])
def submit():
    response = request.form.get('response')
    if response:
        responses.append(response)
        print(f"User response: {response}")  
    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    global responses
    responses = []
    return redirect(url_for('home'))

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/back')
def back():
    if responses:
        responses.pop()  
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
