import tkinter as tk
from tkinter import messagebox
import re
import subprocess
import speech_recognition as sr
from dateutil import parser
import threading
from datetime import datetime

recognizer = sr.Recognizer()

# Initialize variables
reminder_text = ""
date_text = ""
time_text = ""

# Function to open other applications and close the main app
def open_applications_and_quit():
    app_1_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_reminder_play_sound_part.py"
    app_2_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_reminder_app.py"
    app_3_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_sorting_reminder_part.py"

    subprocess.Popen(["python", app_3_path])
    subprocess.Popen(["python", app_2_path])
    subprocess.Popen(["python", app_1_path])
    app.quit()

# Function to save the reminder to a file
def save_reminder(reminder_text, date_text, time_text):
    try:
        # Get the current date and time
        now = datetime.now()
        current_year = now.year
        formatted_date = f"{current_year}-{date_text}"

        # Create the reminder string in the specified format
        reminder_str = f"{formatted_date},{reminder_text},{time_text}\n"
        with open("reminders.txt", "a") as file:
            file.write(reminder_str)

        messagebox.showinfo("Success", "Reminder saved successfully!")
        reminder_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    except Exception as e:
        print(f"Error saving reminder: {e}")

# Function to continuously listen for voice input
def listen_for_voice_input():
    global reminder_text, date_text, time_text

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
            print("Recognizing...")

        try:
            voice_input = recognizer.recognize_google(audio)
            print("You said:", voice_input)

            # First-level checks
            reminder_match = re.search(r'remind me to (.+) on', voice_input)
            time_match = re.search(r'at (\d+:\d+(?: [ampm]*))', voice_input)
            date_match = re.search(r'on (\d+:\d+)', voice_input)

            if reminder_match:
                reminder_text = reminder_match.group(1)
                reminder_entry.delete(0, tk.END)
                reminder_entry.insert(0, reminder_text)
            if time_match:
                # Extract the time string and convert it to 24-hour format
                time_str = time_match.group(1) + 'm'  # Add 'm' to make sure it's a complete time string
                time_obj = datetime.strptime(time_str, '%I:%M %p')
                time_text = time_obj.strftime('%H:%M')
                time_entry.delete(0, tk.END)
                time_entry.insert(0, time_text)
            if date_match:
                date_text = date_match.group(1)
                date_entry.delete(0, tk.END)
                date_entry.insert(0, date_text)

            if reminder_text and date_text and time_text:
                save_reminder(reminder_text, date_text, time_text)
                open_applications_and_quit()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error recognizing audio: {e}")

            # Second-level checks (if the first checks didn't catch it)
            if not reminder_text and "remind me to" in voice_input:
                reminder_text = voice_input.split("remind me to", 1)[1].strip()
                reminder_entry.delete(0, tk.END)
                reminder_entry.insert(0, reminder_text)
            if not time_text and "at" in voice_input:
                time_match_second = re.search(r'at (\d+:\d+)', voice_input.split("at", 1)[1])
                if time_match_second:
                    time_text = time_match_second.group(1)
                    time_entry.delete(0, tk.END)
                    time_entry.insert(0, time_text)
            if not date_text and "on" in voice_input:
                date_match_second = re.search(r'on (\d+:\d+)', voice_input.split("on", 1)[1])
                if date_match_second:
                    date_text = date_match_second.group(1)
                    date_entry.delete(0, tk.END)
                    date_entry.insert(0, date_text)

            if reminder_text and date_text and time_text:
                save_reminder(reminder_text, date_text, time_text)
                open_applications_and_quit()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error recognizing audio: {e}")

def save_button_callback():
    global reminder_text, date_text, time_text
    reminder_text = reminder_entry.get()
    date_text = date_entry.get()
    time_text = time_entry.get()
    save_reminder(reminder_text, date_text, time_text)

# Create the main window
app = tk.Tk()
app.geometry("400x175")
app.title("Voice-Enabled Reminder App")

# Reminder Entry
reminder_label = tk.Label(app, text="Reminder:")
reminder_label.pack()
reminder_entry = tk.Entry(app, width=40)
reminder_entry.pack()

# Date Entry
date_label = tk.Label(app, text="Date (mm:dd):")
date_label.pack()
date_entry = tk.Entry(app, width=10)
date_entry.pack()

# Time Entry
time_label = tk.Label(app, text="Time (hh:mm):")
time_label.pack()
time_entry = tk.Entry(app, width=10)
time_entry.pack()

#Save Button
save_button = tk.Button(app, text="Save", command=save_button_callback)
save_button.pack()

# Quit Button
quit_button = tk.Button(app, text="Quit", command=open_applications_and_quit)
quit_button.pack()

# Start a thread for listening to voice input
voice_thread = threading.Thread(target=listen_for_voice_input)
voice_thread.daemon = True
voice_thread.start()

app.mainloop()