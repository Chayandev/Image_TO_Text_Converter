
from flask import Flask, flash, request, redirect, url_for, render_template
import os
import numpy as np
from werkzeug.utils import secure_filename
import cv2 as cv
from pytesseract import pytesseract as pyt
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
sentence = ""
app.secret_key = "chayan_codeder"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', ])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


def text_detection(in_stream):
    arr = np.fromstring(in_stream, dtype='uint8')
    newImage = cv.imdecode(arr, cv.IMREAD_UNCHANGED)
    global sentence
    sentence = ""

    # newImage = cv.cvtColor(newImage, cv.COLOR_BGR2GRAY)
    # newImage = cv.threshold(
    #     newImage, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]


    letter_data = pyt.image_to_data(
        newImage, config=r'--oem 3 --psm 6', lang='eng')
    sentence = pyt.image_to_string(newImage)
    # s=""
    for i, letter_data in enumerate(letter_data.splitlines()):
        if i != 0:
            r = letter_data.split()
            if len(r) == 12:
                x, y, w, h = int(r[6]), int(r[7]), int(r[8]), int(r[9])
                newImage = cv.rectangle(
                    newImage, (x, y), (x+w, y+h), (0, 0, 255), 1)
                # cv.putText(newImage,(r[11]),(x,y),cv.FONT_HERSHEY_PLAIN,1,(0,0,225))
                # s += r[11]+" "
    # print(s)
    cv.imwrite("static/processed/boxex.jpg", newImage)

    _, out_stream = cv.imencode('.PNG', newImage)

    return out_stream


@app.route('/', methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    # filename=request.form['img-name'] + '.jpg'
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_data = text_detection(file.read())
        filelocation = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filelocation, 'wb')as f:
            f.write(file_data)
        global sentence
        if sentence == "":
            sentence = "No Text to show !"

      #print('upload_image filename: ' + filename)
        flash('✅ Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename, result=sentence)
    else:
        flash('❌ Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
