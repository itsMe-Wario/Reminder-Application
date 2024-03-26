from datetime import datetime

def read_reminders(file_path):
    reminders = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 3:
                print(f"Invalid line in the reminder.txt file: {line}")
                continue

            date_str, text, time_str = parts
            try:
                reminder_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m:%d %H:%M")
                reminders.append((reminder_time, text))
            except ValueError:
                print(f"Invalid date or time format in the reminder.txt file: {line}")
                continue

    except FileNotFoundError:
        print("Failed to read reminder.txt. Please make sure the file exists.")
        exit(1)

    return reminders

def delete_passed_reminders(file_path):
    current_datetime = datetime.now()
    reminders = read_reminders(file_path)

    # Filter out passed reminders for today
    remaining_reminders = [
        (time, text) for time, text in reminders
        if time.date() > current_datetime.date() or
        (time.date() == current_datetime.date() and time.time() > current_datetime.time())
    ]

    # Sort reminders by the time difference (closest reminders first)
    remaining_reminders = sorted(
        [(time, text) for time, text in reminders if time > current_datetime],
        key=lambda x: x[0] - current_datetime
    )

    # Write the updated reminders back to the file
    with open(file_path, 'w') as file:
        for time, text in remaining_reminders:
            file.write(f"{time.strftime('%Y-%m:%d')},{text},{time.strftime('%H:%M')}\n")

if __name__ == "__main__":
    reminder_file = 'reminders.txt'

    # Delete passed reminders and arrange the remaining ones
    delete_passed_reminders(reminder_file)

    print("Reminders processed and updated.")