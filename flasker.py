import os
import flask

from flask import Flask, render_template, jsonify, request, redirect, flash, url_for, json
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_PATH = 'collection'
INDEX_PATH = 'indexstore'
ALLOWED_EXTENSIONS= {'json'}

for dir in [UPLOAD_PATH, INDEX_PATH]:
    for path in os.listdir(dir):
        full_path = os.path.join(dir, path)
        if os.path.isfile(full_path):
            os.remove(full_path)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)


@app.route('/')
def index():
    paths = (os.listdir(UPLOAD_PATH))
    print(paths)
    paths = json.dumps(paths, separators=(',', ':'))
    print(paths)
    return render_template('index.html', collection=paths)

@app.route('/', methods=['POST'])
def upload_file():
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(UPLOAD_PATH, uploaded_file.filename))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)