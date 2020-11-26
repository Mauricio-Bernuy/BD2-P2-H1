from flask import Flask, jsonify, request, redirect
import nltk
import numpy 
import math
import pprint
import pickle
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

import functools

stopfile = "stoplist.txt"
outfile = "invertedindex.txt"

fstop = open(stopfile,'r', encoding='utf-8')
mainfile = open(outfile,'w+', encoding='utf-8')
stoplist = stopwords.words("spanish")
stoplist += fstop.read() #load stoplist
stoplist += ['?','¿','.',',',';','!','¡','«','»',':','(',')','@','rt','#','`','``','"'] #load unnecesary signs

app = Flask(__name__)

UPLOAD_FOLDER = '/uploadedfiles/'
ALLOWED_EXTENSIONS = {'json'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Es la foto de Vizcarra?</title>
    <h1>Cargar una foto y ver si corresponde al presidente Vizcarra!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Cargar">
    </form>
    '''


def detect_faces_in_image(file_stream):

    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    picture_of_vizcarra = face_recognition.load_image_file("fotos_bd/vizcarra.png")    
    known_face_encoding = face_recognition.face_encodings(picture_of_vizcarra)[0]
    

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    
    face_found = False
    is_vizcarra = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        for i in range(len(unknown_face_encodings)):
            match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[i])
        # Your can use the distance to return a ranking of faces <face, dist>. 
        # face_recognition.face_distance([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_vizcarra = True

    # Return the result as json
    result = {
        "rostro_encontrado_en_imagen": face_found,
        "es_foto_de_vizcarra": is_vizcarra
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
