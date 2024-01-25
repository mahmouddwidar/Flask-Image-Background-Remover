import os
import image_processing
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_file
import config

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = config.SECRET_KEY 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('layout.html')

rembg_img_name = None

@app.route('/remback',methods=['POST'])
def remback():
    global rembg_img_name
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        rembg_img_name = filename.split('.')[0]+"_py-removal.png"
        image_processing.remove_background(app.config['UPLOAD_FOLDER'] + '/' + filename, app.config['UPLOAD_FOLDER'] + '/' + rembg_img_name)
        return render_template('home.html',org_img_name=filename,rembg_img_name=rembg_img_name)
    else:
        return '<h1>Invalid Image <br> Please Be Sure its allowed extension [png, jpg, jpeg, webp]</h1>'

@app.route('/download')
def download():
    if rembg_img_name:
        return send_file(f'{app.config["UPLOAD_FOLDER"]}/{rembg_img_name}', as_attachment=True)
    else:
        return "No image available for download."

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])