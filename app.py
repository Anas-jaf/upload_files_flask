from flask import Flask, request, render_template
from tqdm import tqdm
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('./upload_page.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if files are present in the request
    if 'files[]' not in request.files:
        return 'No file selected'
    
    files = request.files.getlist('files[]')
    
    # Create the upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    total_files = len(files)
    
    # Save each file to the upload folder with tqdm progress bar
    for file in tqdm(files, desc='Uploading', unit='file', total=total_files):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    return 'Files uploaded successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
