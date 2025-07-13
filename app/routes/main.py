from platformdirs import user_runtime_dir
from app.service import sherlock
from flask import Blueprint, request, jsonify
import subprocess

main = Blueprint("main", __name__)

@main.route("/", methods=["POST"])
def analyze_user():
    data = request.get_json()

    username = data.get("username")
    about_me = data.get("about_me")

    if not username or not about_me:
        return jsonify({"error": "username and about_me fields are required"}), 400

    user_profiles = sherlock.run_sherlock(username)

    response = generate_prompt(about_me, user_profiles)
    print(f"Generated response: {response}")

    return jsonify({"response": response})

def generate_prompt(about_me, links):
    prompt = f"""
You are a conversation assistant. Based on the following user's 'about me' and social links, suggest 3 interesting conversation topics that we could talk about.

Bio: {about_me}

Social Links: {links}

Respond in bullet points.
DON'T SAY WHY YOU ARE SUGGESTING THESE TOPICS, JUST GIVE THE TOPICS.
"""
    print(f"Prompt for ollama: {prompt}")
    # Call Ollama CLI to run mistral model
    command = ['ollama', 'run', 'mistral']

    try:
        result = subprocess.run(command, input=prompt, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        print(f"Ollama output: {output}")
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error running ollama: {e.stderr}")
        return "Error generating response."
