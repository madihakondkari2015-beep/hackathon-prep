from flask import Flask, request, jsonify, render_template
from ai_helper import (
    calculator_tool,
    weather_tool,
    text_tool,
    wikipedia_tool,
    decide_tool
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "tool_used": "none",
            "response": "Invalid request"
        })

    user_input = data["message"]

    tool = decide_tool(user_input)

    if tool == "calculator":
        result = calculator_tool(user_input)

    elif tool == "weather":
        result = weather_tool()

    elif tool == "text_count":
        result = text_tool("count", user_input)

    elif tool == "text_reverse":
        result = text_tool("reverse", user_input)

    elif tool == "text_uppercase":
        result = text_tool("uppercase", user_input)

    elif tool == "wikipedia":
        topic = user_input.replace("tell me about", "").strip()
        result = wikipedia_tool(topic)

    else:
        result = "Could not determine tool"

    return jsonify({
        "tool_used": tool,
        "response": result
    })


if __name__ == "__main__":
    app.run(debug=True)