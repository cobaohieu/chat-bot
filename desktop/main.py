"""


pip install speechrecognition pyaudio
or
pip3 install speechrecognition pyaudio


"""


import openai
import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something!")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""


def chat_with_openai(text):
    openai.api_key = "Your API Key here"
    messages = [
        {"role": "user", "content": text},
    ]
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    reply = chat.choices[0].message['content']
    return reply


def main():
    text = recognize_speech()
    if text:
        response = chat_with_openai(text)
        print("Chatbot:", response)


if __name__ == "__main__":
    main()



