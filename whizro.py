import speech_recognition as sr
from spellchecker import SpellChecker
import pyttsx3,keyboard
import datetime,time
import shutil
import os,webbrowser
import wikipediaapi

# Initialize speech recognition and text-to-speech synthesis
recognizer = sr.Recognizer()
spell = SpellChecker()
engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
# Create a Wikipedia API object with a custom user agent
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='Your User Agent'
)

# Function to search in Wikipedia
def search_wikipedia(query):
    page = wiki.page(query)
    if page.exists():
        return page.text[0:500]  # Limit the text to the first 500 characters
    else:
        return "Sorry, I couldn't find any information on that topic."

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning sir....")
    elif hour >=12 and hour<18:
        speak("Good Afternoon sir....")
    else:
        speak("Good evening sir....")   
    speak("i am whizro for here to help you...  ")

# Function to listen for voice commands or text
def get_microphone_index():
    devices = sr.Microphone.list_microphone_names()
    print("Available audio input devices:")
    for i, device in enumerate(devices):
        print(f"Index {i}: {device}")

    while True:
        try:
            index = int(input("Enter the index of the desired audio input device: "))
            if 0 <= index < len(devices):
                break
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
    return index


def listen(use_microphone=True):
    recognizer = sr.Recognizer()
    user_input = ""

    if use_microphone:
        try:
            with sr.Microphone(device_index=index) as source:
                print("Listening...")
                recognizer.pause_threshold = 1
                audio = recognizer.listen(source)
                print("Recognizing...")
                user_input = recognizer.recognize_google(audio,language='en-in')
                print("You said:", user_input)
        except sr.UnknownValueError:
            print("Sorry, Say that again please.")
        except sr.RequestError:
            print("Sorry, I am having trouble accessing the speech recognition service.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")
        except OSError:
            print("Error accessing the audio device.")
    else:
        user_input = input("Enter your command: ")

    return user_input

# Function to correct user input
def correct_input(user_input):
    words = user_input.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_input = ' '.join(corrected_words)
    return corrected_input

def set_reminder(reminder_time, reminder_message):
    current_time = datetime.datetime.now()
    reminder_time = datetime.datetime.strptime(reminder_time, "%H:%M")

    if reminder_time < current_time:
        print("The reminder time should be in the future.")
    else:
        time_difference = reminder_time - current_time
        seconds = time_difference.total_seconds()

        print(f"Reminder set for {reminder_time.strftime('%H:%M')} with message: {reminder_message}")

        # Wait for the specified time
        time.sleep(seconds)
        print(f"Reminder: {reminder_message}")    
        
    
# Function to handle user commands
def handle_command(command):
    command=command.lower()
    command = correct_input(command)
    if "hello" in command or 'hi' in command:
        speak("Hello! How can I assist you today?")
        
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")

    elif 'remainder' in command:
        reminder_time = input("Enter the reminder time (HH:MM): ")
        reminder_message = input("Enter the reminder message: ")

        set_reminder(reminder_time, reminder_message)
    elif 'thank you' in command:
        speak("your welcome")

    elif 'wikipedia' in command:
        speak("Searching in Wikipedia...")
        print("Searching in Wikipedia...")
        command = command.replace("wikipedia", "")
        results = search_wikipedia(command)
        speak("According to Wikipedia")
        print("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in command:
        webbrowser.open("youtube.com")  
    elif 'open google' in command:
        webbrowser.com("google.com")      

    else:
        print("Sorry, I couldn't understand your command.")    
        
# Main program loop
if __name__=="__main__":
    wishme() 
    use_microphone = input("Do you want to use the microphone? (y/n): ").lower() == 'y'
    if use_microphone:
        index = get_microphone_index()
    while True:
        # speak("How can I assist you?")
        command = listen(use_microphone).lower
        if 'microphone' in command:
            use_microphone = input("Do you want to use the microphone? (y/n): ").lower() == 'y'
            if use_microphone:
                index = get_microphone_index()
        if 'exit' in command:
            break    
        handle_command(command)    

