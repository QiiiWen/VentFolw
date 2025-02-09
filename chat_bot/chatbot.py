from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Set up OpenAI API Key (Replace with your key)
openai.api_key = "your-api-key"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({"response": response["choices"][0]["message"]["content"]})

if __name__ == "__main__":
    app.run(debug=True)