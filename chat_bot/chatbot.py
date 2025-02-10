import os
from dotenv import load_dotenv
from openai import OpenAI
import mysql.connector
from config import get_db_connection  # Import database connection function

load_dotenv()

# Set OpenAI API Key
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=OPEN_AI_API_KEY)

messages = [
    {"role": "system", "content": "You are an event assistant. Only answer questions about events."}
]

def fetch_event_info(query):
    """Retrieve event details from the database based on user input."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT event_name, description, date, category FROM events WHERE event_name LIKE %s LIMIT 5;", (f"%{query}%",))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    if not results:
        return "I'm sorry, I couldn't find any events matching your query."

    # Format event details into text
    event_details = "\n".join([f"{r['event_name']} - {r['description']}, Date: {r['date']}, Category: {r['category']}" for r in results])
    return f"Here are the matching events:\n{event_details}"

def chat_bot():
    while True:
        message = input("User: ")
        if message.lower() == "quit":
            break

        # Check for event details in the database
        event_info = fetch_event_info(message)

        # Update chat context with event data
        messages.append({"role": "user", "content": f"{message}\n\nDatabase Info: {event_info}"})

        output = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        response = output.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        print("AI:", response)

if __name__ == "__main__":
    chat_bot()