from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from time import sleep
import threading
from ml_model import *

app = Flask(__name__)

upload_folder = 'static\\upload'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

def del_file(path):
    sleep(30)
    os.remove(path)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        img = os.path.join(upload_folder, filename)
        if(img == 'static\\upload\\'):
            return render_template('index.html',vimg = False)
        file.save(img)
        sign = predict(img)
        render = render_template('index.html',vimg = True, img=img, cap = sign)
        # Start a new thread to delete the file after 90 seconds
        deletion_thread = threading.Thread(target=del_file, args=(img,))
        deletion_thread.start()
        return render
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)