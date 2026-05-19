import speech_recognition as sr
from googletrans import Translator 
from gtts import gTTS
from playsound import playsound
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# function for text to speech
def speak(text, lang='en'):
    try:
        # Save to a safe temporary file location instead of Desktop
        filepath = os.path.join("C:\\Users\\DELL", "temp.mp3")

        # Remove if already exists
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except PermissionError:
                print("File in use. Close any app playing 'temp.mp3'")
                return

        # Generate and play audio
    
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)
        playsound(filepath)
        os.remove(filepath)
    except Exception as e:
        print(f"Error in speak(): {e}")

# function to recognize speech input
def listen():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening..")
        
        try: 
            audio=recognizer.listen(source)
            text=recognizer.recognize_google(audio)   #sends your voice to google speech recognition API
            print(f"You said:{text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry I did not understand.Please try again")  
            return listen()
        except sr.RequestError as e:
            print(f"Could not connect to Google: {e}")
            return ""

        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""
       
#function to translate the text
def translate_text(text,target_language):
    translator=Translator()
    translation=translator.translate(text,dest=target_language)
    return translation.text

def collect_feedback():
    print("\n--- Feedback Time ---")
    print("Choose your feedback color:")
    print("Red = Bad")
    print("Orange= Average")
    print("Green = Good")
    print("Blue = Excellent")

    color = input("Enter your feedback color (red/orange/green/blue): ").strip().lower()

def show_feedback_heatmap():
    try:
        df = pd.read_csv('feedback_data.csv')

        # Count feedback occurrences
        pivot = df.pivot_table(index='Color', values='Score', aggfunc='count').fillna(0)

        # Ensure consistent order
        color_order = ['red', 'orange', 'green', 'blue']
        pivot = pivot.reindex(color_order).fillna(0)

        # Convert to 2D array
        data = pivot.values

        # Create a custom color map for each row
        color_map = {
            'red': sns.dark_palette("red", as_cmap=True),
            'orange': sns.dark_palette("orange", as_cmap=True),
            'green': sns.dark_palette("green", as_cmap=True),
            'blue': sns.dark_palette("blue", as_cmap=True)
        }

        # Plot each row separately with its own color
        fig, axes = plt.subplots(nrows=len(color_order), figsize=(6, 6), sharex=True)

        for i, color in enumerate(color_order):
            sns.heatmap(
                np.array([[data[i][0]]]),  # single value as 2D array
                annot=True,
                fmt='g',
                cmap=color_map[color],
                cbar=False,
                ax=axes[i],
                linewidths=1,
                linecolor='black',
                xticklabels=['Count'],
                yticklabels=[color]
            )
            axes[i].set_ylabel(color)
            axes[i].set_xlabel('')

        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No feedback data found yet!")

        plt.title("Feedback Heatmap (Based on Colors)")
        plt.ylabel("Feedback Color")
        plt.xlabel("Count")
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("No feedback data found yet!")

#main function
def main():
    speak("Welcome to language translation bot.")
    print("Welcome to language translation bot.")
    while True:
        speak("please say the text you want to translate. ")
        text_to_translate=listen()
        if text_to_translate.lower()=="exit":
            speak("Goodbye have a great day.")
            show_feedback_heatmap()
            break
        speak("Which language should i translate to? Please say the language code for example 'es' for spanish")
        target_language=input("Please enter the language code:")
        try:
            translated_text=translate_text(text_to_translate,target_language)
            print(f"Translated Text: {translated_text}")
            speak(translated_text, lang=target_language)

        except Exception as e:
            print(f"An error occured: {e}")
            speak(f"an error occured: {e}")
        collect_feedback()
if __name__=="__main__":
    main()

