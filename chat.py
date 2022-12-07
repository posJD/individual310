import json
import re
import random_responses
import requests

bot_name = "gymchatbot"


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


def get_response(msg):
    split_message = re.split(r'\s+|[,;?!.-]\s*', msg.lower())
    score_list = []

    if 'calories' in msg:
        activity = msg.split('in', 1)

        api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity[1])
        response1 = requests.get(api_url, headers={'X-Api-Key': 'VajbNSZZ8lGZ1RqvdCxi7A==h86zPFMKBp9TzM4M'})

        if response1.status_code == requests.codes.ok:
            return response1.text
        else:
            print("Error:", response1.status_code, response1.text)

    if 'quote' in msg:
        activity1 = msg.split('quote', -1)

        api_url = 'https://api.api-ninjas.com/v1/quotes?activity1={}'.format(activity1[-1])
        response2 = requests.get(api_url, headers={'X-Api-Key': 'VajbNSZZ8lGZ1RqvdCxi7A==h86zPFMKBp9TzM4M'})

        if response2.status_code == requests.codes.ok:
            return response2.text
        else:
            print("Error:", response2.status_code, response2.text)

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if msg == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()
