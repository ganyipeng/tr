from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import pdfParser
import uuid
import gyptest
import base64
import idCardRowsParser

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

api = Api(app)

@app.route('/')
def hello_world():
    return render_template('upload.html')

@app.route('/image')
def hello_image():
    return gyptest.test()

@app.route('/id-card-page')
def id_card():
    return render_template('id-card.html')

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

class IdCard(Resource):
  def post(self):
    dict = request.form
    image_base64 = dict['image']
    image_base64_array = image_base64.split('base64,')
    image_type = image_base64_array[0].replace("data:image/", '').replace(";", '')
    image_valid_base64 = image_base64_array[1]
    imgdata = base64.b64decode(image_valid_base64)
    fileName = app.config['UPLOAD_FOLDER'] + str(uuid.uuid1()) + "."+image_type
    file = open(fileName, 'wb')
    file.write(imgdata)
    file.close()
    result = gyptest.test(fileName)
    rows = result['rows']
    id_card_dict = idCardRowsParser.parse(rows)
    return id_card_dict, 200

api.add_resource(Upload, '/upload2')
api.add_resource(IdCard, '/id-card')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
