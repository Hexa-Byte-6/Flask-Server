import os
from flask import Flask, request
from werkzeug.utils import secure_filename 
from flask_pymongo import PyMongo

UPLOAD_FOLDER = 'uploads/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/loginDB"
mongo = PyMongo(app)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FILE_PATH=''


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/admin/login',methods=['POST'])
def loginUser():
   flag = False
   response={}
   if(request.method == 'POST'):
      print(request.get_json())
      requestBody = request.get_json()
      name = requestBody['username']
      password=requestBody['password']
      print("Name: "+name)
      print("Password: "+password)
      prefix = name[0:2] #prefix code of state
      name = name[2:] #actual username to search
      print(prefix)      
      print(name)
      state_users = mongo.db[prefix]
      #query = {'$and':[{'username':name},{'password':password}]}
      for admin in state_users.find():
         print(admin)
         if(admin['username'] == name and admin['password'] == password):
            flag = True
            break
      if flag:
         response['status'] = 1
         response['message'] = "User Authenticated"
      else:
         response['status'] = 0
         response['message'] = "Invalid username or password"
   return response   

@app.route('/api/survey/uploadImage',methods=['POST'])
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
            data = mongo.db.images.insert_one({'image_name':filename,'url':'<server-url>/'+FILE_PATH})
            if(data):
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