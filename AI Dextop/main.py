import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys



engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
# print (voices[0].1d
engine.setProperty('voices',voices[0].id)
# text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.say(audio)
    print(audio)
    engine.runAndWait()
# to convert voice inti text
def takecommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.......")
        r.pause_threshold= 1
        audio = r.listen(source,timeout=1,phrase_time_limit=5)

    try:
        print("Reconizing.......")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said: {query}" )
    except Exception as e:
        speak("Say that again plrase......")
        return "noun"
    return query

# to wish
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

    '''takecommand()
     speak("this is advance a/i")
    while True:'''
    if 1:
        query =takecommand().lower()
        # logic building for tasks
        if "open notepad" in query:
            npath ="C:\\Users\\sinha\\Desktop"
            os.startfile(npath)

        elif "open clock" in query:
            apath = "C:\\Users\\91629\\OneDrive\\Desktop\\Clock.lnk"
            os.startfile(apath)

        elif "open powerpoint" in query:
            bpath = "C:\\Users\91629\\OneDrive\\Desktop\\PowerPoint 2013.lnk"
            os.startfile(bpath)

        elif "open telegram" in query:
            epath = "C:\\Users\\91629\\OneDrive\\Desktop\\Telegram Desktop.lnk"
            os.startfile(epath)

        elif "open facebook" in query:
            fpath = "C:\\Users\\91629\\OneDrive\\Desktop\\Facebook.lnk"
            os.startfile(fpath)

        elif "play music" in query:
            music_dir = "D:\\Music"
            songs = os.listdir(music_dir)
            rd =random.choice(songs)
            os.startfile(os.path.join(music_dir,rd))

        elif "open command from " in query:
            os.startfile("start cmd")


        elif ("open google ")  in query:
            speak("sir, what should I search on google")
            g = takecommand().lower()
            webbrowser.open(f"{g}")
            speak("this is the information")



        elif "ip address" in query:
            ip = get('https://api.ipify.rog').text
            speak(f"your IP address is {ip}")
        elif "wikipedia" in query:
            speak("searching wikipedia......")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentence=2)
            speak("according to wikipedia")
            speak(results)
            print(results)


        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "play song for youtube" in query:
            kit.playonyt("see you again ")






        elif " no thanks " in query:
            speak("thanks for using me sir , have a good day.")
            sys.exit()
        speak("sir, do you have any other work ")

        # elif "sand message" in query:
        #     pywhatkit.sendwhatmsg(",hello "2,25)


        # elif "email to vishajit" in query:
        #     try:
        #         speak(("whit sgould i say "))
        #         content = takecommand().lower()
        #         to = "codearduino7@gmail.com"
        #         sendEail(to,content)
        #         speak("Email has been sent to avi")
        #
        #     except Exception as e:
        #         print(e)
        #         speak("sorry sir ,i am not able to sent this mail to avi")

            







        '''elif "open Word" in query:
            cpath = "C:\\Users\\91629\\OneDrive\\Desktop\\Word 2013.lnk"
            os.startfile(cpath)

        elif "open excel " in query:
            dpath = "C:\\Users\\91629\\OneDrive\\Desktop\\Excel 2013.lnk"
            os.startfile(dpath)

        elif "open telegram " in query:
            epath = "C:\\Users\\91629\\OneDrive\\Desktop\\Telegram Desktop.lnk"
            os.startfile(epath)

        elif "open email " in query:
            fpath = "C:\\Users\\91629\\OneDrive\\Desktop\Mail.lnk"
            os.startfile(fpath)

        elif "open command from " in query:
            os.startfile("start cmd")'''




















































































































