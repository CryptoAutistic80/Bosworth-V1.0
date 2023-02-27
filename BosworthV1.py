 # _____ _______     _______ _______ ____            _    _ _______ _____  _____ _______ _____ _____  
# / ____|  __ \ \   / /  __ \__   __/ __ \      /\  | |  | |__   __|_   _|/ ____|__   __|_   _/ ____| 
#| |    | |__) \ \_/ /| |__) | | | | |  | |    /  \ | |  | |  | |    | | | (___    | |    | || |      
#| |    |  _  / \   / |  ___/  | | | |  | |   / /\ \| |  | |  | |    | |  \___ \   | |    | || |      
#| |____| | \ \  | |  | |      | | | |__| |  / ____ \ |__| |  | |   _| |_ ____) |  | |   _| || |____  
# \_____|_|  \_\ |_|  |_|      |_|  \____/  /_/    \_\____/   |_|  |_____|_____/   |_|  |_____\_____| 
                                                                                                     
                                                                                                     
# ____  _            _        _           _         _____                       _                      
#|  _ \| |          | |      | |         (_)       |_   _|                     (_)                     
#| |_) | | ___   ___| | _____| |__   __ _ _ _ __     | |  _ __ ___   __ _  __ _ _ _ __   ___  ___ _ __ 
#|  _ <| |/ _ \ / __| |/ / __| '_ \ / _` | | '_ \    | | | '_ ` _ \ / _` |/ _` | | '_ \ / _ \/ _ \ '__|
#| |_) | | (_) | (__|   < (__| | | | (_| | | | | |  _| |_| | | | | | (_| | (_| | | | | |  __/  __/ |   
#|____/|_|\___/ \___|_|\_\___|_| |_|\__,_|_|_| |_| |_____|_| |_| |_|\__,_|\__, |_|_| |_|\___|\___|_|   
#                                                                          __/ |                       
#      James Walford 2022                                                                    |___/                        


import openai
import json
from wikidata.client import Client

# Opens the file at the given filepath and returns its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Initializes a Wikidata client
client = Client()
      
# Reads the API key from a file and sets it as the OpenAI API key
openai.api_key = open_file('key_openai.txt')

# Generates a response based on a given prompt using the OpenAI API
def gpt3_completion(prompt, parameters_file='parameters.json'):
    # Load the parameters from the JSON file
    with open(parameters_file, 'r') as parameters_file:
        parameters = json.load(parameters_file)
    
    # Extract the parameters from the dictionary
    engine = parameters.get('engine')
    temp = parameters.get('temp')
    top_p = parameters.get('top_p')
    tokens = parameters.get('tokens')
    freq_pen = parameters.get('freq_pen')
    pres_pen = parameters.get('pres_pen')
    stop = parameters.get('stop', ['Bosworth:', 'User: '])
    
    # Calls the create() method of the Completion class to generate a response
    response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temp,
            max_tokens=tokens,
            top_p=top_p,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            stop=stop)
    # Extracts the generated response from the response object and returns it as a string
    response = response['choices'][0]['text'].strip()
    return response

  
# This block of code is only executed if the script is run directly (not imported as a module)
if __name__ == '__main__':
    # Initializes an empty list to store the conversation
    conversation = list()
    # Continuously prompts the user for input and generates a response
 
    while True:
        # Prompts the user for input and stores it in the conversation list
        user_input = input('\033[92mUser: ')
        conversation.append('\033[92mUser: %s' % user_input)
        print()
        # Reads the prompt template from a file and replaces the placeholder with the current conversation
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        # Appends a newline and the string 'DevBot:' to the prompt to indicate where the response should be inserted
        prompt = prompt + '\nBosworth:'
        # Calls the gpt3_completion() function to generate a response
        response = gpt3_completion(prompt)
        # Prints the response and stores it in the conversation list
        print('\033[94mBosworth:', response, '\033[0m')
        conversation.append('Bosworth: %s' % response)
        print()