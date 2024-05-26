import os
from pathlib import Path

dirpath = r"C:\Users\lauej\Downloads"
os.chdir(dirpath)
files = filter(os.path.isfile, os.listdir(dirpath))
files = [os.path.join(dirpath, f) for f in files] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))

print(files[0:10])