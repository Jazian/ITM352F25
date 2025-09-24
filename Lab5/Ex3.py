# Define a list of survey response values
survey_responses = [5, 7, 3, 8]

#Define a tuple of survey respondent IDs
respondent_ids = (1012, 1035, 1021, 1053)

# Create a dictionary by zipping together the list and tuple with IDS as the keys and responses as values
survey_dict = dict(zip(respondent_ids, survey_responses))
print("Survay response vales", survey_responses)
print("Survey respondent IDs", respondent_ids)
print("Survey dictionary", survey_dict)

print(f"Respondent ID {respondent_ids[2]} gave a response of {survey_dict[respondent_ids[2]]}")