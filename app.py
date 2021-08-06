from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import pdfParser
import uuid
import gyptest

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

api = Api(app)

@app.route('/')
def hello_world():
    return render_template('upload.html')

@app.route('/image')
def hello_image():
    return gyptest.test()

class Upload(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    args = parser.parse_args()
    file = args['file']
    if file.filename.endswith(".png"):
        fileName = str(uuid.uuid1())+".png"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
        result = gyptest.test(r"./upload/"+fileName)
        return result, 201
    fileName = str(uuid.uuid1())+".pdf"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    result = pdfParser.pdf2json(r"./upload/"+fileName[0:-4])
    # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fileName[0:-4])+'.docx')
    return result, 201

api.add_resource(Upload, '/upload2')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
