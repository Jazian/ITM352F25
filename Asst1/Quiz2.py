# Quiz 2. Put questions and answers into a list
# Jazian Uejo
# Date: 10/3/25

QUESTIONS = [
    ("What is the airspeed of an unladen swallow in miles/hr", "12"),
    ("What is the capital of Texas", "Austin"),
    ("The last supper was painted by which atist", "Da Vinci")
]

for question, correct_answer in QUESTIONS:
    answer = input(f"{question}?")
    if answer == correct_answer:
        print("Correct")
    else:
        print(f"The answe is {correct_answer!r}, not {answer!r}")