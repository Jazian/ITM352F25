# Quiz 6, Put questions and answers into a dictionary, to include other options
# Allow user to choose correct answer by its label
# Improve look and usability. Keept track of answers.
# Loop until the user provides a valid answer
# Randomize the order of questions and numbers
# Name: Jazian Uejo
# Date: 10/8/2025

from string import ascii_lowercase
import random

# Quiz qustions for each question list the possible answers, with the first answer being 

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "24", "36", "48"],
    "What is the capital of Texas": ["Austin", "Dallas", "Houston", "Waco"],
    "The last supper was painted by which atist": ["Da Vinci", "Michelangelo", "Raphael", "Leonardo"],
    "Which classic novel opens with the line 'Call Me Ishmal'": ["Mobi Dick", "Pride and Joy", "Random book3", "RandomBook4"]
}

num_correct = 0
NUM_QUESTIONS_PER_QUIZ = 5
num_questions = min(NUM_QUESTIONS_PER_QUIZ, len(QUESTIONS))
# Randomly select a subset of questions for the quiz
questions = random.sample(list(QUESTIONS.items()), num_questions)

for num, (question, alternatives) in enumerate(questions, 1):
    print(f"\nQuestion {num}:")
    print(f"{question}? ")

    correct_answer = alternatives[0]
    labelled_alternatives = dict(zip(ascii_lowercase, random.sample(alternatives, len(alternatives))))
    for label, alternatives in labelled_alternatives.items():
        print(f" {label} - {alternatives}")

    while (answer_label := input("\nChoice? ")) not in labelled_alternatives:
        print(f"Please answer one of {', '.join(labelled_alternatives)}")
    answer = labelled_alternatives.get(answer_label)
    
    if answer == correct_answer:
        print("* Correct! *")
        num_correct += 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")

print (f"\nYou got {num_correct} out of {len(questions)} questions correct.")