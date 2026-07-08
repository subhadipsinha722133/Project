import pyttsx3
import speech_recognition as sr
import os


engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)   # voice

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshold= 1
        audio = r.listen(source,timeout=1,phrase_time_limit=5)

    try:
        print("Recognizing.......")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said: {query}" )
    except Exception as e:
        speak("Say that again please......")
        return "none"
    return query

import datetime

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak("good morning")
    elif hour > 12 and hour < 18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak('I am Smart AI sir. Please tell me how can I help you')

if __name__ == "__main__":
    wish()

    # takecommand()
    #  speak("this is advance a/i")
    # while True:
    if 1:
        query =takecommand().lower()
        # logic building for tasks
        if "open notepad" in query:
            npath ="C:\\Users\\sinha\\Desktop\\Notepad.lnk"
            os.startfile(npath)
        
        elif "open Github" in query:
            apath = "C:\\Users\\sinha\\Desktop\\GitHub.lnk"
            os.startfile(apath)

        # elif "open powerpoint" in query:
        #     bpath = "C:\\Users\91629\\OneDrive\\Desktop\\PowerPoint 2013.lnk"
        #     os.startfile(bpath)

        # elif "open telegram" in query:
        #     epath = "C:\\Users\\91629\\OneDrive\\Desktop\\Telegram Desktop.lnk"
        #     os.startfile(epath)

        # elif "open facebook" in query:
        #     fpath = "C:\\Users\\91629\\OneDrive\\Desktop\\Facebook.lnk"
        #     os.startfile(fpath)















if __name__ == "__main__":
    takecommand()
    # speak(" hello")
