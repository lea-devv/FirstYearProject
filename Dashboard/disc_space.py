from matplotlib.figure import Figure
import numpy as np
import sqlite3
import shutil
import base64
import io

#matplotlib.use('Agg')

class Storage:
    def __init__(self, db_directory, file_directory):
        self.db_directory = db_directory
        self.file_directory = file_directory

    def storage_graph(self):
        global free_storage_gb
        total, used_storage_b, free_storage_b = shutil.disk_usage(self.file_directory)
        used_storage_gb = used_storage_b // (2**30)
        free_storage_gb = free_storage_b // (2**30)
        
        y = np.array([(used_storage_gb), (free_storage_gb)])
        labels = ["Used GB", "Free GB"]

        fig =  Figure()

        ax = fig.subplots()
        ax.pie(y, labels=labels, autopct=lambda p : '{:.1f} GB'.format(p * sum(y) / 100))
        ax.axis('equal')  
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        
        img = base64.b64encode(buf.getvalue()).decode('utf-8')
        return img


    def days_to_full(self):
        conn = sqlite3.connect(self.db_directory)
        cur = conn.cursor()
        cur.execute("SELECT storage_used_today_gb FROM daily_change_count")
        data = cur.fetchmany(7)
        conn.close()
            
        total_weekly_storage_gb = 0
        for row in data:
             total_weekly_storage_gb += row[0]
        print(total_weekly_storage_gb)
        calculated_to_full = free_storage_gb / total_weekly_storage_gb
        rounded_days = round(calculated_to_full)

        return(rounded_days)
