import win32com.client
import speech_recognition as sr
import os
import webbrowser
import subprocess
import sys
import datetime
import openai
from config import apikey
import random
import threading

chatStr = ""  
stop_speaking = threading.Event() 

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    chunks = text.split('. ')  
    for chunk in chunks:
        if stop_speaking.is_set():
            break
        speaker.Speak(chunk)
        if stop_speaking.is_set():
            break

def listen_for_stop_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while not stop_speaking.is_set():
            try:
                audio = r.listen(source, timeout=1)
                query = r.recognize_google(audio, language='en-in')
                if "alright Jarvis" in query.lower() or "stop here Jarvis" in query.lower():
                    stop_speaking.set()
                    break
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Nivas: {query}\nJarvis: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        response_text = response["choices"][0]["message"]["content"]
        stop_speaking.clear()  # Reset the stop event
        speak_thread = threading.Thread(target=say, args=(response_text,))
        stop_thread = threading.Thread(target=listen_for_stop_command)

        speak_thread.start()
        stop_thread.start()

        speak_thread.join()
        stop_speaking.set()  # Ensure stop_speaking is set after speaking
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print("Error:", e)
        return "Sorry, I could not process your request."

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response: {prompt} \n************************************\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        response_text = response["choices"][0]["message"]["content"]
        print(response_text)
        text += response_text
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{random.randint(1, 1000000)}.txt", "w") as f:
            f.write(text)
    except Exception as e:
        print("Error:", e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "None"
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return "None"

if __name__ == '__main__':
    print('Assistant')
    say("Hello Sir. I am Jarvis")

    while True:
        query = takeCommand()
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["Google", "https://www.google.com"],
            ["LinkedIn", "https://www.linkedin.com"],
            ["NCMCargo", "https://www.ncmcargo.com"]
        ]
        if query != "None":
            for site in sites:
                if site[0].lower() in query.lower():
                    say(f"Opening {site[0]} Sir...")
                    webbrowser.open(site[1])

            if "open music" in query.lower():
                musicPath = r"C:\Users\NIVAS\OneDrive\Desktop\Dell Laptop\Desktop\Anne-Marie - Then.mp3"
                if sys.platform == "win32":
                    os.startfile(musicPath)
                else:
                    opener = "xdg-open"
                    subprocess.call([opener, musicPath])

            elif "time" in query.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the time is {strTime}")

            elif "your intelligence" in query.lower():
                ai(prompt=query)

            elif "buy jarvis" in query.lower():
                exit()

            elif "reset chat" in query.lower():
                chatStr = ""

            else:
                print("Chatting...")
                chat(query)
