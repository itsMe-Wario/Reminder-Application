import subprocess

def stop_first_app():
    # Write to a file to signal the first app to stop
    with open("stop_signal.txt", "w") as stop_file:
        stop_file.write("stop")

# After stopping, you can restart the first app
def restart_first_app():
    subprocess.Popen(["python","final_reminder_play_sound_part.py"])

print("Stopped and reopened.")
