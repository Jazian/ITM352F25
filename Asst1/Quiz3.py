# Quiz 3, Put questions and answers into a dictionary, to include other options
# Name: Jazian Uejo
# Date: 10/3/2025

# Quiz qustions for each question list the possible answers, with the first answer being 

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "24", "36", "48"],
    "What is the capital of Texas": ["Austin", "Dallas", "Houston", "Waco"],
    "The last supper was painted by which atist": ["Da Vinci", "Michelangelo", "Raphael", "Leonardo"]
}

for question, alternatives in QUESTIONS.items():
    correct_answer = alternatives[0]
    for alternatives in sorted(alternatives):
        print(f" - {alternatives}")

    answer = input(f"{question}? ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")