# Quiz 10, Utilizing Quiz 8 as the base file and adding the additional assignments specified by my student ID.
# 1. Write the history of scores out to a file. (Done in Quiz 9)
# 5. Allow the user to choose a category for their questions, e.g. history, art, modern politics, NBA trivia, NFL trivia, music trivia, etc. 
# Name: Jazian Uejo
# Date: 10/8/2025

from string import ascii_lowercase
import random
import json

# Quiz qustions for each question list the possible answers, with the first answer being the correct answer
question_file = open('CategoryQuestions.json', 'r')
QUESTIONS = json.load(question_file)
question_file.close()

# Ask user to choose a category
available_categories = list(QUESTIONS.keys())
category_choice = input(f"Please choose a category from: {available_categories}\n> ")

while category_choice not in available_categories:
    category_choice = input(f"Please choose a category from: {available_categories}\n> ")
    if category_choice not in available_categories:
        print("Invalid category. Please try again.")

# Prepare a list of questions
def prepare_questions(questions, num_questions):
    num_questions = min(num_questions, len(questions))
    # Randomly select a subset of questions for the quiz
    return random.sample(list(questions.items()), num_questions)

# Get an answer from the user ensuring it is one of the valid choices.
def get_answer(question, alternatives):
    print(f"\n{question}?")
    labelled_alternatives = dict(zip(ascii_lowercase, random.sample(alternatives, len(alternatives))))
    for label, alternatives in labelled_alternatives.items():
        print(f" {label} - {alternatives}")
    
    #Loop until the user provides a valid answer
    while (answer_label := input("\nChoice? ")) not in labelled_alternatives:
        print(f"Please answer one of {', '.join(labelled_alternatives)}")
    return labelled_alternatives.get(answer_label)

def ask_question(question, alternatives):
    correct_answer = alternatives[0]
    ordered_alternatives = random.sample(alternatives, len(alternatives))
    answer = get_answer(question, ordered_alternatives)

    if answer == correct_answer:
        print("* Correct *")
        return 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")
        return 0

num_correct = 0
NUM_QUESTIONS_PER_QUIZ = 5

# Main Quiz Loop
# Changed questions = prepare_questions(QUESTIONS, NUM_QUESTIONS_PER_QUIZ) to include specific category choices before randomizing
questions = prepare_questions(QUESTIONS[category_choice], NUM_QUESTIONS_PER_QUIZ)
for num, (question, alternatives) in enumerate(questions, 1):
    print(f"\nQuestion {num}:")
    num_correct += ask_question(question, alternatives)
    

print (f"\nYou got {num_correct} out of {len(questions)} questions correct.")

# Creates a new file that holds previous scores
# To reset the scores delete score_history.txt
score_file = open("score_history.txt", "a")
score_file.write(f"{num_correct} out of {len(questions)} correct\n")
score_file.close()
