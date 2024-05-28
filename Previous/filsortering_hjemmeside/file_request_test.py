import datetime
import os

class Recent_Files:
    def __init__(self, dirpath, amount):
        global dir_info
        self.dirpath = dirpath
        self.range_amount = amount
        dir_info = os.walk(self.dirpath)
   
    def get_recent_files(self):
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

#Recent_Files.changes_by_date()

        


