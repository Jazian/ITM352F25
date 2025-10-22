# Save the dictionary of quiz questions as a JSON file

import json

QUESTIONS = {
    "What is the airspeed of an unladen swallow in miles/hr": ["12", "24", "36", "48"],
    "What is the capital of Texas": ["Austin", "Dallas", "Houston", "Waco"],
    "The last supper was painted by which artist": ["Da Vinci", "Michelangelo", "Raphael", "Leonardo"],
    "Which classic novel opens with the line 'Call Me Ishmael'": ["Moby Dick", "Pride and Prejudice", "Random book3", "RandomBook4"]
}

JSON_file = "quiz.json"
with open(JSON_file, 'w') as jsonfile:
    json.dump(QUESTIONS, jsonfile, indent=4)

print(f"Quiz questions saved to {JSON_file}")