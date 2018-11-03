import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory,render_template
from werkzeug.utils import secure_filename
import hashlib
import filecmp


UPLOAD_FOLDER = 'upload'
HASH_FOLDER = 'hash'
ALLOWED_EXTENSIONS =(['txt','pdf','png','log','jpg','jpeg','gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HASH_FOLDER'] = HASH_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.secret_key = b'_5#y2LF4Q8zec'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

def comparehash(new_hash):
    filels = os.listdir(os.path.join(app.config['HASH_FOLDER']))
    print(new_hash)
    bfile = open(new_hash, 'rb')
    print (bfile.read())
    print(filels)
    for file in filels:
        print (file)
        x = filecmp.cmp(new_hash,os.path.join(app.config['HASH_FOLDER'],file))
        print (x)
        if x:
            print (new_hash.split('/',1)[1].lower())
            print (file.lower())
            if new_hash.split('/',1)[1].lower() == file.lower():
                flash ('file already uploaded')
                return False

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            x = hashfile(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            h = open(os.path.join(app.config['HASH_FOLDER'], filename) + '.md5', "w")
            h.write(x)
            h.close()
            if not(comparehash(os.path.join(app.config['HASH_FOLDER'], filename) + '.md5')):
                return redirect(request.url)
            return redirect(url_for('uploaded_file', filename=filename))
        if file:
            flash('File type not permitted')
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/list/')
def filelist():
    filels = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
    return render_template('files.html', files=filels)

@app.route('/delete/')
def deletelist():
    filels = os.listdir(os.path.join(app.config['UPLOAD_FOLDER']))
    return render_template('delete.html', files=filels)

@app.route('/delete/<item_id>')
def delete_file(item_id):
    print (item_id)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item_id))
    try:
        os.remove(os.path.join(app.config['HASH_FOLDER'], item_id)+'.md5')
    except:
        pass
    return redirect(url_for('deletelist'))

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)


