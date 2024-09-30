import openai
import datetime
import math
import time 
import json
import tiktoken
from utils import *
from dotenv import load_dotenv

# Replace your key here 
load_dotenv()
openai.organization = os.getenv('OPENAI_ORGANIZE')
openai.api_key = os.getenv('OPENAI_API_KEY')

def count_tokens(message):
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens_integer= encoding.encode(message)
    return len(tokens_integer)

def count_chat_history_tokens(chat_history):
    total_tokens = 0
    for message in chat_history:
        total_tokens += count_tokens(message['content'])
        total_tokens += count_tokens(message['role'])
    
    return total_tokens

def truncate_message(message, n):
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens_integer = encoding.encode(message)
    if len(tokens_integer) <= n:
        return False, None
    else:
        truncated_tokens = tokens_integer[:math.floor(n)]
        truncated_message = encoding.decode(truncated_tokens)
        return True, truncated_message

def process_history(prompt, history, max_tokens, threshold):
    tokens_in_chat_history = count_chat_history_tokens(history)
   
    if tokens_in_chat_history > math.floor(max_tokens*threshold):
        last_prompt_message = history[-1]['content'] 
        if count_tokens(last_prompt_message ) > 4000:
            del history[-1]
            truncated, truncated_message = truncate_message(last_prompt_message, (max_tokens-count_chat_history_tokens(history))*threshold)
            history.append({"role": "user", "content": truncated_message})
        
        print('summarize==========================================')
        history.append({"role": "user", "content": 'The conversation is about to exceed the limit, before we continue the reproduction process. Can you summarize the above conversation. Note that You shouldn\'summary the rule and keep the rules as original since the rules are the standards.'})
        response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=history,
                max_tokens=max_tokens-count_chat_history_tokens(history)-300,
                n=1,
                stop=None,
                temperature=0.3,
            )
        message = response["choices"][0]["message"]["content"]
        print(message)
        history = load_training_prompts('./training_prompts_ori.json')
        history.append({"role": "user", "content": message})
       
    history.append({"role": "user", "content": prompt})
  
    return history

def generate_text(prompt, history, package_name=None, model="gpt-4", max_tokens=128000, attempts = 3):
    
    history = process_history(prompt, history, max_tokens, threshold = 0.75)

    for times in range(attempts):  # retry up to 3 times
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=history,
                #max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.3,
            )
            return response, history
        except openai.OpenAIError as e:
            print(f"Attempt {times + 1} failed with error: {str(e)}")
            if times < 2: 
                if package_name is not None:
                    save_chat_history(history, package_name)
                print(f"Take a 60*{times+1} seconds break before the next attempt...")
                time.sleep(60*(times+1)) 
            else: 
                print(f"All {attempts} attempts failed. Please try again later.")
                if package_name is not None:
                    save_chat_history(history, package_name)
                raise e




def save_chat_history(history, package_name):
    curr_time = datetime.datetime.now()
    curr_time_string = curr_time.strftime("%Y-%m-%d %H-%M-%S")
    file_name = f"./chat_history/{package_name}_chat_{curr_time_string}.json"
    with open(file_name, 'w') as file:
        json.dump(history, file)

def get_model_name(response):
     model_name = response["model"]
     return model_name

def get_message(response):
    message = response["choices"][0]["message"]["content"]
    return message


