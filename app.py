import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)


UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = 'mp3'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            y, sr = librosa.load(filename)
            D = np.abs(librosa.stft(y))
            librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
            plt.title('Power spectrogram')
            plt.colorbar(format='%+2.0f dB')
            plt.tight_layout()

            image_name = filename.split('.')[0] + '.png'
            plt.savefig('static/images/' + image_name)

            os.remove(filename)

            return render_template('image_template.html', user_image='static/images/' + image_name)

    return render_template('base.html')
