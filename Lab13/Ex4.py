from flask import Flask, render_template, request, redirect, url_for, session
import json, random
from string import ascii_lowercase

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

with open('CategoryQuestions.json', 'r') as f:
    QUESTIONS = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form['category']
        session['category'] = category
        session['questions'] = random.sample(list(QUESTIONS[category].items()), 5)
        session['current'] = 0
        session['score'] = 0
        return redirect(url_for('quiz'))
    return render_template('indexQuiz.html', categories=QUESTIONS.keys())

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if session['current'] >= len(session['questions']):
        return redirect(url_for('results'))

    if request.method == 'POST':
        selected = request.form.get('answer')
        q, options = session['questions'][session['current']]
        correct = options[0]
        if selected == correct:
            session['score'] += 1
        session['current'] += 1
        return redirect(url_for('quiz'))

    q, options = session['questions'][session['current']]
    shuffled = random.sample(options, len(options))
    return render_template('quiz.html', question=q, options=shuffled, q_num=session['current'] + 1)

@app.route('/results')
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    with open("score_history.txt", "a") as f:
        f.write(f"{score} out of {total} correct\n")
    return render_template('results.html', score=score, total=total)

if __name__ == '__main__':
    app.run(debug=True)
