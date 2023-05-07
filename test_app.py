import unittest
import requests
import os
from app import app


class TestApp(unittest.TestCase):
    def test_chatgpt_api_integration(self):
        prompt = "Code:\ndef my_function():\n    print('Hello, world!')\n\nOutput:"
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
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, world!", response.json()["choices"][0]["text"])

    def test_homepage_rendering(self):
        client = app.test_client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>ChatGPT API Example</h1>", response.data)

    def test_results_page_rendering(self):
        client = app.test_client()
        data = {"message": "print('Hello, world!')"}
        response = client.post("/results", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<p>You entered:</p>", response.data)
        self.assertIn(b"<p>The AI generated:</p>", response.data)


if __name__ == "__main__":
    unittest.main()
