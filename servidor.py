import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from recognizer_heimdall import recognize
import cv2
from azure.storage.blob.blockblobservice import BlockBlobService
import imutils
from lector import read
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR,"heimdall","uploads")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
blob_service = BlockBlobService(account_name="pulpo", account_key="99gcpDXzMldXARK5zbdoeSCIP/vGXsf/WIlB43vZ8kcau6AVO9/xunneq56VezHReTUxMzWCd7ZPc77Nnri2iA==")
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/recognize', methods=['GET', 'POST'])
def recognize_view():                                               
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("asdas")
            filename = secure_filename(file.filename)
            file_path= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            file.save(file_path)
            f = cv2.imread(file_path) 
            rotated = imutils.rotate_bound(f, 270)
            cv2.imwrite(file_path,rotated)
            return recognize(file_path)
        return "failed"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/read', methods=['GET', 'POST'])
def read_book():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            f = cv2.imread(file_path) 
            rotated = imutils.rotate_bound(f, 270)
            cv2.imwrite(file_path,rotated)
            blob_service.create_blob_from_path("impakto",file.filename,file_path)
            return read("https://pulpo.blob.core.windows.net/impakto/"+file.filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>c
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)