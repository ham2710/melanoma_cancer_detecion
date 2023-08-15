import os
from flask import Flask, flash, request, redirect, render_template, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import random, string
from pathlib import Path
import psycopg2
from models.file_model import Files
from db.db import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from settings import Config
import classify_models

# printing lowercase
letters = string.ascii_lowercase
print ( ''.join(random.choice(letters) for i in range(10)) )
app=Flask(__name__)
app.config.from_object('settings.Config')
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'static')

FILE_FOLDER = "static"

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

db.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect("/")

        files = request.files.getlist('files[]')
        try:
            for file in files:
                if file and allowed_file(file.filename):
                    
                    filename = secure_filename(file.filename)
                    file_name, file_extension = os.path.splitext(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    #cur = index()
                    file_entry = Files(file_name=filename)
                    file_entry.file_path = os.path.join(app.config['UPLOAD_FOLDER'])
                    file_entry.file_ext = file_extension
                    db.session.add(file_entry)
                    db.session.commit()
                else :
                    flash('File not upload Successfully !', "danger")
                    return render_template('upload.html')
            flash('File upload Successfully !', "success")
        except IntegrityError as e:
                flash('Something went wrong please try again later', "danger")
                print("Error: ",e)
                return redirect(request.url)
        files_list = Files.query.all()
        return render_template('upload.html', files_list=files_list)

@app.route('/get_file_details', methods=['GET'])
def get_file_data():
    
    if request.method == 'GET':
        
        thisdict = {
            "data": []
        }

        data_list = thisdict.get("data")
        entries = Path(os.path.join(app.config['UPLOAD_FOLDER']))
        
        files_list = Files.query.order_by(None).order_by(Files.created_at.desc())
        print("harshik",files_list)
        for row in files_list:
            
            names_file = {
                "name":row.file_name,
                "view":row.file_id
            }
            data_list.append(names_file)
        
        thisdict.update(data_list)
        print(thisdict)
    return jsonify(thisdict)
'''
@app.route('/', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('upload.html')
'''
@app.route('/get_image_data', methods=['POST', 'GET'])
def get_image_data():
    print("Image id: ",request.get_json().get('id'))
    adr = request.get_json().get('id')
    result = Files.query.filter(Files.file_id==adr)
    
    for row in result:
        file_name = row.file_name
        image_details = row
    
    print("image: ",UPLOAD_FOLDER+"/"+ file_name)
    cancer_type = classify_models.predict_cancer(FILE_FOLDER+"/"+file_name)
    return jsonify({ 'image_name': image_details.file_name , 
                    'cancer_type': cancer_type})
    #return render_template('upload.html', image_details= image_details)

@app.route('/delete_image', methods=['POST','GET'])
def delete_image():
    print("delete Image id: ",request.get_json().get('id'))
    adr = request.get_json().get('id')

    with Session(engine) as session, session.begin():
        session.execute(delete(Files).where(Files.file_id == adr))
        print("delete Image id: ",adr)
        session.commit()

    Files.query.filter(Files.file_id == adr).delete()
    return render_template('upload.html')
    #return render_template('upload.html', image_details= image_details)


def remove_img(self, path, img_name):
    os.remove(UPLOAD_FOLDER + '/' + img_name)
# check if file exists or not
    if os.path.exists(path + '/' + img_name) is False:
        # file did not exists
        return True

def random_string():
    return ''.join(random.choice(letters) for i in range(50))

if __name__ == "__main__":
    letters = string.ascii_lowercase
    app.secret_key = random_string()
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["SESSION_PERMANENT"] = False
    Session(app)
    app.run(host='127.0.0.1',port=5005,debug=True,threaded=True)