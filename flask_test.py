from file_request import Recent_Files

recent_files_list = Recent_Files("C:/Users/lauej/Downloads/", 100)
files_returned = recent_files_list.get_recent_files()
for x in range(len(files_returned)):
    print(files_returned[x])

