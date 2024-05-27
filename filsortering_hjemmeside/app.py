from flask import Flask, render_template
from file_request_test import Recent_Files 
app = Flask(__name__)

@app.route('/')
def home():
    recent_files_list = Recent_Files("C:/Users/frago\Documents", 10)
    files_returned = recent_files_list.get_recent_files()
    
    return render_template('recent_files.html', files=files_returned)

if __name__ == '__main__':
    app.run(debug=True)