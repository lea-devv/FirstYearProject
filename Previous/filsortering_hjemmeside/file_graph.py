import datetime
import os
from matplotlib import pyplot as plt
from collections import defaultdict
from io import BytesIO
import matplotlib.ticker as ticker
import base64
from matplotlib.figure import Figure



class Recent_Files:
    def __init__(self, dirpath, amount):
        global dir_info
        self.dirpath = dirpath
        self.range_amount = amount
        dir_info = os.walk(self.dirpath)
   
    def get_recent_files(self):
        file_changes = defaultdict(int)
        for dirpath, dirnames, filenames in dir_info:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    m_time = os.path.getmtime(filepath)
                    dt_m = datetime.datetime.fromtimestamp(m_time).date()  # Use date instead of datetime
                    file_changes[dt_m] += 1
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
        return file_changes
    
    def plot_file_changes(self):
        file_changes = self.get_recent_files()
        days = sorted(file_changes.keys())  # Sort dates to ensure chronological order
        counts = []
        total_changes = 0
        for day in days:
            total_changes += file_changes[day]
            counts.append(total_changes)
        fig = Figure()
        fig.subplots_adjust(bottom=0.3)
        ax = fig.subplots()
        ax.tick_params(axis='x', which='both', rotation=30)
        ax.set_facecolor("#fff")
        ax.plot(days, counts)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5, prune='both'))
        ax.set_title('Changes pr. day')
        ax.set_xlabel("Date")
        ax.set_ylabel("No. of files changed")
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
        

#recent_files = Recent_Files("C:/Users/lauej/Downloads/", 10)
#recent_files.plot_file_changes()

        


