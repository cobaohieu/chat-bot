"""


app.py


"""

from flask import Flask, render_template, request
import openai
import os
import speech_recognition as sr
import pyttsx3


app = Flask(__name__,template_folder='templates')


def config(api_key):
    openai.api_key = api_key
    #openai.api_key = os.getenv(api_key)
    openai.Model.list()


def chat_with_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use the appropriate engine for your use case
        prompt=prompt,
        max_tokens=150,  # Adjust the response length as needed
        stop=None  # You can add custom stop words to prevent GPT-3 from continuing indefinitely
    )
    return response.choices[0].text.strip()


def save_to_history(user_input, chatbot_response):
    with open('history.txt', 'a', encoding='utf-8') as file:
        file.write(f"You: {user_input}\nChatbot: {chatbot_response}\n\n")


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

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # You can adjust the speech rate as needed
    engine.say(text)
    engine.runAndWait()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']

    # Check if the user input starts with "speech: " to trigger speech-to-text
    if user_input.lower().startswith("speech:"):
        user_input = speech_to_text()
        if not user_input:
            # If speech recognition failed, return an error message
            return "Sorry, please check your speaker."

    prompt = f"You: {user_input}\Boo said :"
    response = chat_with_gpt3(prompt)
    save_to_history(user_input, response)
    text_to_speech(response)  # Speak the chatbot's response
    return response


if __name__ == "__main__":
    config('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')  # Replace 'YOUR_API_KEY' with your actual API key
    app.run(host='0.0.0.0', port=88888, debug=True)  # Run the Flask app in debug mode for development purposes
