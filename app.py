from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

import requests

def generate_response(prompt):
    try:
        response = requests.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            },
            json={
                "prompt": prompt,
                "max_tokens": 1024,
                "n": 1,
                "stop": None,
                "temperature": 0.5,
            },
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error: something went wrong."



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    message = request.form['message']
    prompt = f"Code:\ndef my_function():\n    {message}\n\nOutput:"
    try:
        response = generate_response(prompt)
        return render_template('results.html', message=message, response=response)
    except Exception as e:
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
