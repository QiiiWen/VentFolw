import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key = OPEN_AI_API_KEY)

messages = [
    { "role": "system", "content": "You are a sarcastic assistant!" } # testing only, to be changed...
]

def chat_bot():
    while True:
        message = input("User: ")
        if message.lower() == "quit":
            break
        messages.append( { "role": "user", "content": message } )
        output = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages = messages
        )
        messages.append({ "role": "assistant", "content": output.choices[0].message.content })
        print(output.choices[0].message.content)

if __name__ == "__main__":
    chat_bot()