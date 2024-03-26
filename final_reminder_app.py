import tkinter as tk
from tkinter import messagebox
import datetime
import subprocess

REMINDERS_FILE = 'reminders.txt'

def load_reminders():
    reminders = {}
    try:
        with open(REMINDERS_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    date_str, task, time_str = parts
                    date = datetime.datetime.strptime(date_str, "%Y-%m:%d")
                    time_obj = datetime.datetime.strptime(time_str, "%H:%M")

                    # Check if the date already exists in reminders
                    if date not in reminders:
                        reminders[date] = []

                    reminders[date].append({'task': task, 'time': time_obj.strftime("%H:%M")})
    except FileNotFoundError:
        pass
    return reminders

def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as file:
        for date, reminder_list in reminders.items():
            date_str = date.strftime("%Y-%m:%d")
            for reminder in reminder_list:
                time = reminder['time']
                task = reminder['task']
                file.write(f"{date_str},{task},{time}\n")

def add_reminder():
    task = task_entry.get()
    time_str = time_entry.get()
    date_str = date_entry.get()

    try:
        current_year = datetime.datetime.now().year
        reminder_date = datetime.datetime.strptime(f"{current_year}-{date_str}", "%Y-%m:%d")
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")

        # Check if the date already exists in reminders
        if reminder_date not in reminders:
            reminders[reminder_date] = []

        reminders[reminder_date].append({'task': task, 'time': time_obj.strftime("%H:%M")})
        save_reminders(reminders)
        messagebox.showinfo("Success", "Reminder added successfully!")
        task_entry.delete(0, 'end')
        time_entry.delete(0, 'end')
        date_entry.delete(0, 'end')
    except ValueError:
        messagebox.showerror("Error", "Invalid time or date format. Use HH:MM format for time and MM-DD format for date.")

def delete_reminder():
    date_str = date_entry.get()
    
    try:
        current_year = datetime.datetime.now().year
        reminder_date = datetime.datetime.strptime(f"{current_year}-{date_str}", "%Y-%m:%d")
    
        if reminder_date in reminders:
            del reminders[reminder_date]
            save_reminders(reminders)
            messagebox.showinfo("Success", "Reminder deleted successfully!")
            date_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Reminder not found for the given date.")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use MM-DD format.")

def change_reminder():
    date_str = date_entry.get()
    
    try:
        current_year = datetime.datetime.now().year
        reminder_date = datetime.datetime.strptime(f"{current_year}-{date_str}", "%Y-%m:%d")
        if reminder_date in reminders:
            new_text = task_entry.get()
            time_str = time_entry.get()
            try:
                time_obj = datetime.datetime.strptime(time_str, "%H:%M")
                reminders[reminder_date] = {'task': new_text, 'time': time_obj.strftime("%H:%M")}
                save_reminders(reminders)
                messagebox.showinfo("Success", "Reminder changed successfully!")
                task_entry.delete(0, 'end')
                time_entry.delete(0, 'end')
                date_entry.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM format.")
        else:
            messagebox.showerror("Error", "Reminder not found for the given date.")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use MM-DD format.")

def list_reminders():
    reminder_list.delete(0, 'end')
    if reminders:
        for date, reminder_list_for_date in sorted(reminders.items()):
            for reminder in reminder_list_for_date:
                reminder_list.insert('end', f"{date.strftime('%Y-%m-%d')}: {reminder['task']} at {reminder['time']}")
    else:
        reminder_list.insert('end', "No reminders found.")

def open_applications():
    app_4_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\close_sound.py"
    subprocess.Popen(["python", app_4_path])
    app_2_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_sorting_reminder_part.py"
    subprocess.Popen(["python", app_2_path])
    app_3_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\final_reminder_play_sound_part.py"
    subprocess.Popen(["python", app_3_path])

def go_back():
    app_1_path = "D:\\pythonProject\\reminder_app\\Final_work_tkinter\\finalspeech_recog.py"
    subprocess.Popen(["python", app_1_path])


def add_reminder_combined():
    open_applications()
    add_reminder()

def delete_reminder_combined():
    open_applications()
    delete_reminder()
    
def list_reminders_combined():
    open_applications()
    list_reminders()
        
def change_reminder_combined():
    change_reminder()
    list_reminders_combined()

def quit_app():
    root.destroy()

def quit_app_combined():
    open_applications()
    quit_app()

def go_back_combined():
    go_back()
    quit_app()

reminders = load_reminders()

root = tk.Tk()
root.geometry("250x450")
root.title("Reminder App")

# Create and configure the GUI elements
task_label = tk.Label(root, text="Task:")
task_label.pack()
task_entry = tk.Entry(root)
task_entry.pack()

time_label = tk.Label(root, text="Time (HH:MM format):")
time_label.pack()
time_entry = tk.Entry(root)
time_entry.pack()

date_label = tk.Label(root, text="Date (MM:DD format):")
date_label.pack()
date_entry = tk.Entry(root)
date_entry.pack()

go_back_button = tk.Button(root, text="Voice Detect", command=go_back_combined)
go_back_button.pack()

add_button = tk.Button(root, text="Add Reminder", command=add_reminder_combined)
add_button.pack()

delete_button = tk.Button(root, text="Delete Reminder", command=delete_reminder_combined)
delete_button.pack()

change_button = tk.Button(root, text="Change Reminder", command=change_reminder_combined)
change_button.pack()

list_button = tk.Button(root, text="List Reminders", command=list_reminders_combined)
list_button.pack()

quit_button = tk.Button(root, text="Quit", command=quit_app_combined)
quit_button.pack()

reminder_list = tk.Listbox(root)
reminder_list.pack()

root.mainloop()