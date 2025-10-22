# Read a file of questions from a JSON file and save them in a dictionary: Print the dictionary to the console

import json

JSON_file = "quiz.json"
with open(JSON_file, 'r') as json_file:
    questions_dict = json.load(json_file)

print(questions_dict)
    
