import datetime
import os

class Recent_Files:
    def __init__(self, dirpath) -> None:
        self.dirpath = dirpath

    def get_recent_files(self):
        files_with_dates = []

        for dirpath, dirnames, filenames in os.walk(self.dirpath):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    m_time = os.path.getmtime(filepath)
                    dt_m = datetime.datetime.fromtimestamp(m_time)
                    files_with_dates.append((filename, dt_m))
                except FileNotFoundError:
                    print(f"File not found: {filepath}")

        files_with_dates.sort(key=lambda x: x[1], reverse=True)

        #dt_m for modified date, filename for filename
        return files_with_dates
