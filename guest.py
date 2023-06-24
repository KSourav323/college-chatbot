from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import pandas as pd
import json

# Importing the dataset
dataset = pd.read_csv('stud.csv', sep=',')

# Create a new instance of a ChatBot
bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.95
        }
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter"
)

list_trainer = ListTrainer(bot)

with open('intents.json', 'r') as file:
    intents = json.load(file)['intents']

for intent in intents:
    patterns = intent['patterns']
    responses = intent['responses']

    for pattern in patterns:
        list_trainer.train([
            pattern,
            *[response.strip() for response in responses]
        ])




# while True:
#     try:
#         user_input = input('\n> ')
#         response = bot.get_response(user_input)

#         print(response)

#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break
