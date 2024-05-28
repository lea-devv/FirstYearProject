from flask import Flask, render_template
from file_request_test import Recent_Files 
from file_graph import Recent_Files as RF
app = Flask(__name__)

@app.route('/')
def home():
    recent_files_list = Recent_Files("C:/Users/Lau/Music/", 10)
    files_returned = recent_files_list.get_recent_files()
    file_changes1 = RF("C:/Users/Lau/Music/", 10)
    file_changes2 = file_changes1.plot_file_changes()
    return render_template('recent_files.html', file_changes = file_changes2, files = files_returned)

if __name__ == '__main__':
    app.run(debug=True)