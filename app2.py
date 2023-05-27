from flask import Flask, request, render_template
import os
from tqdm import tqdm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where uploaded files will be stored
# app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Set maximum file size to 100MB

@app.route('/')
def home():
    return render_template('upload_page.html')

def save_file_with_progress(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_size = int(request.headers['Content-Length'])

    with open(file_path, 'wb') as f:
        while True:
            chunk = file.stream.read(8192)
            if not chunk:
                break
            f.write(chunk)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        total_files = len(files)
        
        if files:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            for file in tqdm(files, desc='Uploading', unit='file', total=total_files):
                save_file_with_progress(file)
            return 'Files uploaded successfully!'
    return render_template('upload_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
