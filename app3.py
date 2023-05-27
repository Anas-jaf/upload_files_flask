from flask import Flask, request, render_template
import os
from tqdm import tqdm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder where uploaded files will be stored

@app.route('/')
def home():
    return render_template('upload_page.html')

def save_file(file, progress_bar):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(file_path, 'wb') as f:
        while True:
            chunk = file.stream.read(8192)
            if not chunk:
                break
            f.write(chunk)
            progress_bar.update(len(chunk))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        total_files = len(files)
        
        if files:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            total_size = sum(file.content_length for file in files)
            pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Uploading')
            for file in files:
                save_file(file, pbar)
            pbar.close()
            return 'Files uploaded successfully!'
    return render_template('upload_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
