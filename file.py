import os,hashlib,filecmp,time,pathlib
from flask import Flask, flash, request, redirect, url_for, send_from_directory,render_template
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'upload'
HASH_FOLDER = 'hash'
ALLOWED_EXTENSIONS =(['txt','pdf','png','log','jpg','jpeg','gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HASH_FOLDER'] = HASH_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.secret_key = b'_5#y2LF4Q8zec'
pathlib.Path('temp').mkdir(parents=True, exist_ok=True) 
pathlib.Path('blob').mkdir(parents=True, exist_ok=True) 
pathlib.Path('upload').mkdir(parents=True, exist_ok=True) 
pathlib.Path('hash').mkdir(parents=True, exist_ok=True) 

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
    bfile = open(new_hash, 'rb')
    for file in filels:
        x = filecmp.cmp(new_hash,os.path.join(app.config['HASH_FOLDER'],file))
        if x:
            return file
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
            link = os.path.join('upload', filename)
            tmp_file = os.path.join('temp', filename)
            tmp_hash = os.path.join('temp', filename) + '.md5'
            blobname = str(time.time())
            blob_path = os.path.join('blob',blobname)
            blob_hash_path = os.path.join('hash',blobname) + '.md5' 

            file.save(tmp_file)
            x = hashfile(tmp_file)
            h = open(tmp_hash, "w")
            h.write(x)
            h.close()
            samehash = comparehash(tmp_hash)
            print (samehash)
            if samehash:
                if tmp_hash.split('/',1)[1].lower() == samehash.lower():
                    flash ('file already uploaded')
                    os.remove(tmp_hash)
                    os.remove(tmp_file)
                else:
                    os.remove(tmp_hash)
                    os.remove(tmp_file)
                    os.symlink('../blob/'+samehash,link)
                    return redirect(request.url)
            os.rename(tmp_file,blob_path)
            os.rename(tmp_hash,blob_hash_path)
            os.symlink('../'+blob_path,link)
            flash(filename + ' uploaded')
            return redirect(url_for('upload_file'))
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
