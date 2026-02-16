import pyttsx3

def play_sound(text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)       # speed
        engine.setProperty('volume', 1)     # 0..1
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # pick voice by index


        engine.say(text)
        engine.runAndWait()

