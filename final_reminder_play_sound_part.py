from datetime import datetime, timedelta
import time
import threading
import pygame
import tkinter as tk
import subprocess
import os
import signal

# Initialize Pygame mixer once at the beginning
pygame.mixer.init()

# Global variable to indicate if the app should stop
stop_signal = False

# Function to play background music
def play_song():
    pygame.mixer.music.load('sunflower_street.mp3')
    pygame.mixer.music.play(-1)

# Function to stop background music
def stop_song():
    pygame.mixer.music.stop()

# Function to close the popup
def close_pop_up(top):
    top.destroy()

# Function to open another application
def open_applications():
    app_path = os.path.join("D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_sorting_reminder_part.py")
    subprocess.Popen(["python", app_path])

# Function to check reminders
def check_reminders():
    try:
        with open("reminders.txt", "r") as file:
            lines = file.readlines()

        reminders = []
        current_time = datetime.now()

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 3:
                print(f"Invalid line in the remind.txt file: {line}")
                continue

            date_str, reminder, time_str = parts
            try:
                desired_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m:%d %H:%M")
                reminders.append((desired_time, reminder))
            except ValueError:
                print(f"Invalid date or time format in the remind.txt file: {line}")
                continue

        if not reminders:
            print("No future reminders found in remind.txt.")
            return

        time_to_sleep = max(0, (reminders[0][0] - current_time).total_seconds())

        print(f"Waiting for {time_to_sleep} seconds for the next event '{reminders[0][1]}' at {reminders[0][0]}...")
        time.sleep(time_to_sleep)

        threading.Thread(target=show_gui, args=(reminders[0][1],)).start()

    except FileNotFoundError:
        print("Failed to read remind.txt. Please make sure the file exists.")
        exit(1)

# Function to quit the combined actions
def quit_combined(top):
    stop_song()
    close_pop_up(top)
    open_applications()
    # Add any additional cleanup code here

# Function to display a reminder popup
def show_gui(reminder):
    root = tk.Tk()
    root.withdraw()

    # Custom toplevel window with Quit button
    top = tk.Toplevel(root)
    top.geometry("150x70")
    top.title("Reminder")
    tk.Label(top, text=f"Time for event '{reminder}'").pack()

    play_song()  # Play the song when the popup shows up

    quit_button = tk.Button(top, text="Quit", command=lambda: quit_combined(top))
    quit_button.pack()

    root.mainloop()

# Set up a signal handler for SIGTERM (terminate signal)
def handle_stop_signal(signum, frame):
    global stop_signal
    stop_signal = True

signal.signal(signal.SIGTERM, handle_stop_signal)

# Main loop: Check for reminders every 3 seconds
while not stop_signal:
    check_reminders()
    time.sleep(3)
