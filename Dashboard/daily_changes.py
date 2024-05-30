from matplotlib.figure import Figure
import matplotlib.ticker as Ticker
from datetime import datetime
from io import BytesIO
import sqlite3
import base64
import os

class Daily_Changes:
    def __init__(self, db_directory, file_directory , graph_age):
        self.db_directory = db_directory
        self.file_directory = file_directory
        self.graph_age = graph_age

    def setup_database(self):
        try:
            print(self.db_directory)
            conn = sqlite3.connect(self.db_directory) 
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS daily_change_count (date_today TEXT PRIMARY KEY, 
                        change_count INTEGER NOT NULL, storage_used_today_gb REAL NOT NULL);""")
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()

    def log_changes(self):
        dir_temp = os.walk(self.file_directory)
        date_today = datetime.now().date().isoformat()
        self.setup_database()
        files_changed_today = 0
        storage_used_today_B = 0
        storage_used_today_GB = 0


        for dirpath, dirnames, filenames in dir_temp:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    m_time = os.path.getmtime(filepath)
                    m_date = datetime.fromtimestamp(m_time).date().isoformat()

                    if m_date == date_today:
                        files_changed_today += 1
                        file_size = os.path.getsize(filepath)
                        storage_used_today_B += file_size

                except FileNotFoundError:
                    print(f"File not found: {filepath}")

        storage_used_today_GB = storage_used_today_B / (1024 * 1024 * 1024)

        try:
            conn = sqlite3.connect(self.db_directory)
            cur = conn.cursor()
            cur.execute("""INSERT INTO daily_change_count(date_today, change_count, storage_used_today_gb) VALUES(?, ?, ?) 
                        ON CONFLICT(date_today) DO UPDATE SET change_count=excluded.change_count, storage_used_today_gb=excluded.storage_used_today_gb""", 
                        (date_today, files_changed_today, storage_used_today_GB))
            conn.commit()

        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()

    def daily_changes_graph(self):
        conn = sqlite3.connect(self.db_directory)
        cur = conn.cursor()
        cur.execute("SELECT date_today, change_count FROM daily_change_count ORDER BY date_today ASC")
        data = cur.fetchmany(self.graph_age)
        conn.close()

        dates = [row[0] for row in data]
        no_of_changes = [row[1] for row in data]

        fig = Figure()
        fig.subplots_adjust(bottom=0.3)
        ax = fig.subplots()
        ax.tick_params(axis='x', which='both', rotation=30)
        ax.set_facecolor("#fff")

        ax.plot(dates, no_of_changes)

        ax.set_title('Changes per day')
        ax.set_xlabel("Date")
        ax.set_ylabel("No. of files changed")
        ax.xaxis.set_major_locator(Ticker.MaxNLocator(nbins=5, prune='both'))

        buf = BytesIO()
        fig.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return data
