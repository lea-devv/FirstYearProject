import datetime
import os

# Initialize an empty list to hold tuples of (filename, modification time)
files_with_dates = []

for dirpath, dirnames, filenames in os.walk(r"C:\Users\lauej\Downloads"):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        try:
            # Get the file modification timestamp
            m_time = os.path.getmtime(filepath)
            # Convert timestamp into DateTime object
            dt_m = datetime.datetime.fromtimestamp(m_time)
            # Append the filename and its modification time as a tuple
            files_with_dates.append((filename, dt_m))
        except FileNotFoundError:
            print(f"File not found: {filepath}")

# Sort the list of tuples by the modification time
files_with_dates.sort(key=lambda x: x[1], reverse=True)

# Print sorted filenames along with their modification dates
for filename, dt_m in files_with_dates[:10]:
    print(f'Modified on: {dt_m} for file: {filename}')