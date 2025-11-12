# Web front end fro the quiz application
from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)

@app.route('/')
def home():     # Display a welcome page to the user with a Start Quiz link
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():     # Display quiz questions and handle user answers
    global question_num, score

    if request.method == 'POST':
        # Process submitted answers
        the_answer = request.form.get('answer')
        if (the_answer == QUESTIONS[questions[question_num-1][0]][0]):
            # Increment the score
            score += 1
            the_result = "Correct!"
        else:
            the_result = "Incorrect!"
        # Display feedback to the user
        return render_template('question_result.html', question_result=the_result, question=questions[question_num-1][0], answer=the_answer)
    
    question_num += 1
        # Determine if the quiz is over
    if question_num >= len(questions):
            return redirect(url_for('result'))
        
    next_question = questions[question_num-1][0]
    ordered_alternatives = random.sample(questions[question_num-1][1], len(questions[question_num-1][1]))
    return render_template('quiz.html', num=question_num, question=next_question, options=ordered_alternatives)

@app.route('/result')
def result():   # Display the quiz results to the user
    global score, question_num

    template = render_template('result.html', score=score, total=len(questions))
    # Reset for next quiz
    score = 0
    question_num = 0
    return template

# Function to prepare quiz questions
def prepare_questions(all_questions, num_questions):
    num_questions = min(num_questions, len(all_questions))
    return random.sample(list(all_questions.items()), num_questions)

# Main Quiz Steps: prepare questions, run the quiz, give feedback.
# Read in the quiz questions from a JSON file
NUM_QUESTIONS_PER_QUIZ = 5
question_file = open('questions.json')
QUESTIONS = json.load(question_file)
print(f'Loaded {len(QUESTIONS)} questions.')
questions = prepare_questions(QUESTIONS, NUM_QUESTIONS_PER_QUIZ)

question_num = 0
score = 0

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
    