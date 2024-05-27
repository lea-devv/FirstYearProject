import datetime
import os

class Recent_Files:
    def __init__(self, dirpath, amount):
        self.dirpath = dirpath
        self.range_amount = amount

    def get_recent_files(self):
        files_with_dates = []
        listt = []
        print(self.dirpath)
        dir_info = os.walk(self.dirpath)
        for dirpath, dirnames, filenames in dir_info:
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    m_time = os.path.getmtime(filepath)
                    dt_m = datetime.datetime.fromtimestamp(m_time)
                    files_with_dates.append((filename, dt_m))
                    #print(dt_m)
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
        #print(dt_m, files_with_dates)
        files_with_dates.sort(key=lambda x: x[1], reverse=True)

        for filename, dt_m in files_with_dates[:self.range_amount]:
            tupple = (f'Modified on: {dt_m} for file: {filename}')
            listt.append(tupple)
        return listt
            #print(dt_m, filename)
        #dt_m for modified date, filename for filename
        #for x in range(self.range_amount):
        #    temp = files_with_dates[x]
        #    temp_list = []
        #    formated_files_with_dates = temp_list.append(temp)
        #
        #return(formated_files_with_dates)
