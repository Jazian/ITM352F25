# Quiz 4, Put questions and answers into a dictionary, to include other options
# Allow user to choose correct answer
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
    sorted_alternatives = sorted(alternatives)
    for label, alternatives in enumerate(sorted_alternatives,1):
        print(f" {label} - {alternatives}")

    answer_label = int(input(f"{question}? "))
    answer = sorted_alternatives[answer_label -1]
    
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}")