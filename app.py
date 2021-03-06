import os
import zipfile
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from graph import open_zip, read_csv, compress_it, delete_folder, find_temp

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('error'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('error'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            delete_folder(UPLOAD_FOLDER)

            open_zip(os.path.join(UPLOAD_FOLDER, filename), UPLOAD_FOLDER)
            read_csv()
            
            temp_folder = compress_it(filename)

            #return render_template('index.html', name='confirm')

            return redirect('/success/'+ filename)
        
        else: return redirect('/error/File not Allowed')
    return render_template('index.html')

@app.route('/error/')
@app.route('/error/<name>')
def error(name=None):
    return render_template('error.html', name=name)

@app.route('/success/')
@app.route('/success/<name>')
def success(name=None):
    return render_template('index.html', name=name)
    #return send_from_directory(temp_folder + '/', filename, as_attachment=True)

@app.route('/download_file/<filename>')
def download_file(filename):
    ##temp_folder = compress_it(filename)
    temp_folder = find_temp(UPLOAD_FOLDER)
    return send_from_directory(temp_folder + '/', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)