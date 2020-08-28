from flask import Flask, request, redirect, render_template, url_for
from flask.helpers import flash
import numpy as np
from werkzeug.utils import secure_filename
import cv2

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOAD_FOLDER = "tmp_images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def initialize_app(**kwargs):
    app = Flask(__name__)
    app.config.update(kwargs)
    return app


app = initialize_app(
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
)


def is_file_allowed(filename):
    filename = filename.lower()
    return '.' in filename and \
        filename.split('.')[-1] in ALLOWED_EXTENSIONS


def read_image_file(request):
    image_file = request.files.get('file', None)
    filename = secure_filename(image_file.filename)
    if not(image_file and is_file_allowed(filename)):
        print("Bad input file")
        return None
    # image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = np.frombuffer(image_file.read(), np.uint8)
    image_decoded = cv2.imdecode(image, -1)
    return image_decoded


def determine_dominate_color(image):
    print(type(image), image.shape, image.dtype)



@app.route("/api/determine_dominate_color", methods=['POST'])
def determine_dominate_color_api():
    image = read_image_file(request)
    if image is None:
        return "File is empty / Bad image"
    determine_dominate_color(image)
    return "determined"


@app.route("/test/form/upload_image", methods=['GET'])
def show_upload_form():
    return render_template("upload.html")


@app.route("/test/form/upload_image", methods=['POST'])
def determine_dominate_color_form():
    return redirect('/api/determine_dominate_color', code=307)


@app.route("/")
def app_root():
    return redirect("/test/form/upload_image", code=307)


if __name__ == "__main__":
    app.run(debug=True)
    