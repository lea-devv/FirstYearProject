from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from collections import defaultdict
from io import BytesIO
from datetime import date
import datetime
import sqlite3
import base64
import uuid
import os

########################################################################################
def setup_database():
    try:
        conn = sqlite3.connect("C:/Users/Lau/Documents/GitHub/FirstYearProject/restart/database/file_changes.db")  # Create or connect to the database
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS file_modifications
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    path TEXT NOT NULL, 
                    modification_date TEXT NOT NULL 
                    )''')
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()

setup_database()

########################################################################################


class Recent_Files:
    def __init__(self, dirpath, amount):
        global dir_info
        self.dirpath = dirpath
        self.range_amount = amount
        dir_info = os.walk(self.dirpath)
    
    ####################################################################################

    def print_recent_files(self):
        file_info = []
        file_list = []

        for dirpath, dirnames, filenames in dir_info:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    m_time = os.path.getmtime(filepath)
                    dt_m = datetime.datetime.fromtimestamp(m_time).replace(microsecond=0)
                    file_info.append((filename, dt_m))
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
        
        file_info.sort(key=lambda x: x[1], reverse=True)

        for filename, dt_m in file_info[:self.range_amount]:
            tupple = (f'Modified on: {dt_m} for file: {filename}')
            file_list.append(tupple)
        
        return file_list
    
    ####################################################################################
    
    def get_recent_files(self):
        file_info = []
        file_list = []
        file_changes = defaultdict(int)

        for dirpath, dirnames, filenames in dir_info:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    conn = sqlite3.connect("C:/Users/Lau/Documents/GitHub/FirstYearProject/restart/database/file_changes.db")
                    cur = conn.cursor()
                    print("Connected to database\n")
                    
                    try:
                        m_time = os.path.getmtime(filepath)
                        dt_m = datetime.datetime.fromtimestamp(m_time).replace(microsecond=0)
                        file_info.append((filename, dt_m))
                    
                        m_time = os.path.getmtime(filepath)
                        modification_date = datetime.datetime.fromtimestamp(m_time).date().isoformat()
                        
                        cur.execute("""SELECT * FROM file_modifications;""")
                        data = cur.fetchall()
                        if data == []:
                            print("No data in database. Made first insert.")
                            print(filepath, modification_date)
                            cur.execute("""INSERT INTO file_modifications(path, modification_date) VALUES(?,?)""", (filepath, modification_date))
                            conn.commit() 

                        else:
                            for row in data:
                                db_path = row[1]
                                db_modification_date = row[2]
                                if db_path != filepath and db_modification_date != modification_date:
                                    cur.execute("""INSERT INTO file_modifications(path, modification_date) VALUES(?, ?)""", (filepath, modification_date))
                                    conn.commit() 
                            print("1")

                    except FileNotFoundError:
                        print(f"File not found: {filepath}")
                            
                except sqlite3.Error as sql_e:
                    print(f"sqlite error occured: {sql_e}")
                    conn.rollback()
                except Exception as e:
                    print(f"Error occured: {e}")
                except FileNotFoundError:
                    print(f"File not found at {filepath}")
                finally:
                    conn.close()
                
        file_info.sort(key=lambda x: x[1], reverse=True)

        for filename, dt_m in file_info[:self.range_amount]:
            tupple = (f'Modified on: {dt_m} for file: {filename}')
            file_list.append(tupple)
        
        return file_list


    def plot_file_changes(self):
        conn = sqlite3.connect("C:/Users/Lau/Documents/GitHub/FirstYearProject/restart/database/file_changes.db")
        cur = conn.cursor()
        cur.execute("SELECT filepath, modification_date FROM file_modifications ORDER BY modification_date ASC")


        fig = Figure()
        fig.subplots_adjust(bottom=0.3)
        ax = fig.subplots()
        ax.tick_params(axis='x', which='both', rotation=30)
        ax.set_facecolor("#fff")
        ax.plot(1, 2)
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5, prune='both'))
        ax.set_title('Changes pr. day')
        ax.set_xlabel("Date")
        ax.set_ylabel("No. of files changed")
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
        

func = Recent_Files("C:/Users/Lau/Music/", 10)
func.get_recent_files()
        


