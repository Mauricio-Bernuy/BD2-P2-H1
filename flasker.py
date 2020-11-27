import os
import flask

from flask import Flask, render_template, jsonify, request, redirect, flash, url_for, json
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_PATH = 'collection'
INDEX_PATH = 'indexstore'
QUERY = 'query'
ALLOWED_EXTENSIONS= {'json'}

def createpaths():
    for dir in [UPLOAD_PATH, INDEX_PATH]:
        if not os.path.exists(dir):
            os.makedirs(dir)

createpaths()

def clearfiles():
    for dir in [UPLOAD_PATH, INDEX_PATH]:
        for path in os.listdir(dir):
            full_path = os.path.join(dir, path)
            if os.path.isfile(full_path):
                os.remove(full_path)
clearfiles()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import inv_index_functions

query_result_json = []

app = Flask(__name__)

@app.route('/')
def index():
    global query_result_json
    send = query_result_json
    query_result_json = []
    paths = (os.listdir(UPLOAD_PATH))
    print(paths)
    paths = json.dumps(paths, separators=(',', ':'))
    print(paths)
    return render_template('index.html', collection=paths, query_result_json=send)

@app.route('/', methods=['POST'])
def upload_file():
    clearfiles()
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(UPLOAD_PATH, uploaded_file.filename))
    print("building index")
    inv_index_functions.index_build()
    print("index built")
    print("merging index")
    inv_index_functions.mergedindex = inv_index_functions.merge(inv_index_functions.indexstore_dir)
    print("index merged")
    print("generating norm")
    inv_index_functions.generate_norm(inv_index_functions.mergedindex,inv_index_functions.norm)
    print("norm generated")
    print("ready to query")
    return redirect(url_for('index'))

@app.route('/query', methods=['POST'])
def query():
    global query_result_json
    print(request.form['query_search'])
    print('executing query')
    result = inv_index_functions.search(request.form['query_search'], inv_index_functions.mergedindex)
    print('query finished')
    result_json = json.dumps(result, separators=(',', ':'))
    print(result_json)
    f = open("result.json", "w")
    f.write(result_json)
    f.close()
    query_result_json = result_json
    return redirect(url_for('index'))

if __name__ == "__main__":    
    app.run(debug=False)