# Quiz 4, Put questions and answers into a dictionary, to include other options
# Allow user to choose correct answer by its label
# Improve look and usability. Keept track of answers.
# Loop until the user provides a valid answer
# Name: Jazian Uejo
# Date: 10/3/2025

from string import ascii_lowercase

# Quiz qustions for each question list the possible answers, with the first answer being 

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "24", "36", "48"],
    "What is the capital of Texas": ["Austin", "Dallas", "Houston", "Waco"],
    "The last supper was painted by which atist": ["Da Vinci", "Michelangelo", "Raphael", "Leonardo"]
}

num_correct = 0
for num, (question, alternatives) in enumerate(QUESTIONS.items(), 1):
    print(f"\nQuestion {num}:")
    print(f"{question}? ")

    correct_answer = alternatives[0]
    labelled_alternatives = dict(zip(ascii_lowercase, sorted(alternatives)))
    for label, alternatives in labelled_alternatives.items():
        print(f" {label} - {alternatives}")

    answer_label = input("\nChoice? ")
    answer = labelled_alternatives.get(answer_label)
    
    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")

    print (f"\nYou got {num_correct} out of {len(QUESTIONS)} questions correct.")