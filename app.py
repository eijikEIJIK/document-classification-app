import os
import shutil
from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename
import model
import zipfile
from io import BytesIO

#http://127.0.0.1:5000/

app=Flask(__name__)
UPLOAD_FOLDER = 'upload'
DOCUMENT_FOLDER = 'output/document'
OTHERS_FOLDER = 'output/others'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCUMENT_FOLDER'] = DOCUMENT_FOLDER
app.config['OTHERS_FOLDER'] = OTHERS_FOLDER

@app.route('/')
def index():
    #フォルダ初期化
    if os.path.exists(app.config['UPLOAD_FOLDER']):
      shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    if os.path.exists(app.config['DOCUMENT_FOLDER']):
      shutil.rmtree(app.config['DOCUMENT_FOLDER'])
    os.makedirs(app.config['DOCUMENT_FOLDER'], exist_ok=True)
    if os.path.exists(app.config['OTHERS_FOLDER']):
      shutil.rmtree(app.config['OTHERS_FOLDER'])
    os.makedirs(app.config['OTHERS_FOLDER'], exist_ok=True)
    return render_template('index.html')

@app.route('/upload',methods=["post"])
def upload():
    files = request.files.getlist('file')
    for file in files:
        if (os.path.splitext(file.filename)[1]==".jpg"):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))

    model.get_document_img()
    return render_template('download.html')
    

@app.route('/download_document')
def download_document():
    data_files = os.listdir(app.config['DOCUMENT_FOLDER'])
    memory_file = BytesIO() # メモリ上に作成
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf: # 圧縮する
        os.chdir(app.config['DOCUMENT_FOLDER']) # データ格納ディレクトリへ移動
        for individualFile in data_files:
            zf.write(individualFile)
        os.chdir('../../')
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='documents.zip', as_attachment=True)

@app.route('/download_others')
def download_others():
    data_files = os.listdir(app.config['OTHERS_FOLDER'])
    memory_file = BytesIO() # メモリ上に作成
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf: # 圧縮する
        os.chdir(app.config['OTHERS_FOLDER']) # データ格納ディレクトリへ移動
        for individualFile in data_files:
            zf.write(individualFile)
        os.chdir('../../')
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='images.zip', as_attachment=True)

if __name__=='__main__':
    app.run()



