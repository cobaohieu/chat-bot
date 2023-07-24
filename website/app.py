"""


app.py


"""

from flask import Flask, render_template, request
import openai
import speech_recognition as sr


app = Flask(__name__)


def config(api_key):
    openai.api_key = api_key

def chat_with_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use the appropriate engine for your use case
        prompt=prompt,
        max_tokens=150,  # Adjust the response length as needed
        stop=None  # You can add custom stop words to prevent GPT-3 from continuing indefinitely
    )
    return response.choices[0].text.strip()


def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio).lower()
        print("You:", user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    prompt = f"You: {user_input}\nChatbot:"
    response = chat_with_gpt3(prompt)
    return response


if __name__ == "__main__":
    config('YOUR_API_KEY')  # Replace 'YOUR_API_KEY' with your actual API key
    app.run(debug=True)  # Run the Flask app in debug mode for development purposes
