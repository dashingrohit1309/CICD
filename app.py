import os
from flask import Flask, render_template, request, jsonify
from google import genai


app = Flask(__name__)

# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("signup.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    question = data.get("message", "")

    if not question:
        return jsonify({"response": "Please enter a message."})

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=question
        )

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
