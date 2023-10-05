import pyttsx3
from time import sleep
from threading import Thread



def intro_voice():   
    converter = pyttsx3.init()
    converter.setProperty('rate', 180)
    converter.setProperty('volume', 1.0)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    converter.say("Hello!")
    converter.say("""Welcome to our website.""")
    converter.say("I am Amanza, Your virtual assistant.")
    sleep(1)
    converter.runAndWait()

def predicted_voice(text1):
    text1 = text1
    #text22 = text22
    converter = pyttsx3.init()
    converter.setProperty('rate', 180)
    converter.setProperty('volume', 1.0)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    converter.say(text1)
    #converter.say(text22)
    sleep(1)
    converter.runAndWait()