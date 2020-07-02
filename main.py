import os
from flask import Flask, request
from werkzeug.utils import secure_filename 
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/imageDB";
mongo = PyMongo(app)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FILE_PATH=''


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadImage',methods=['POST'])
def save_image():
   print('...Request received')
   if(request.method=='POST'):
      if request.files:
         file = request.files['image-file']
         print(file.filename)
         if(allowed_file(file.filename)):
            filename = secure_filename(file.filename)
            FILE_PATH = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(FILE_PATH)
            data = mongo.db.images.insert({'image_name':filename,'url':'<server-url>/'+FILE_PATH})
            res="Image saved"
         else:
            res="Unsupported image format"
      else:
         res = "No file received"
   print('........')
   
   return res

if __name__ == '__main__':
   app.debug = True 
   app.run(host='192.168.43.117',port=5000)