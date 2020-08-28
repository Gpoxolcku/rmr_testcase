import cv2
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, render_template

from process import determine_dominate_color

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOAD_FOLDER = "tmp_images"
ALLOWED_EXTENSIONS = {'png'}


def initialize_app(**kwargs):
    app = Flask(__name__)
    app.config.update(kwargs)
    return app


app = initialize_app(
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
    UPLOAD_FOLDER=UPLOAD_FOLDER,
)


def is_file_allowed(filename, allowed_extentions=['png']):
    filename = filename.lower()
    return '.' in filename and \
        filename.split('.')[-1] in allowed_extentions


def read_image_file(request):
    image_file = request.files.get('file', None)
    filename = secure_filename(getattr(image_file, "filename", ""))
    if not(image_file and is_file_allowed(filename, ALLOWED_EXTENSIONS)):
        print("Bad input file")
        return None
    # image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = np.frombuffer(image_file.read(), np.uint8)
    image_decoded = cv2.imdecode(image, -1)
    image_decoded = cv2.cvtColor(image_decoded, cv2.COLOR_BGR2RGB)
    return image_decoded


@app.route("/api/determine_dominate_color", methods=['POST'])
def determine_dominate_color_api():
    image = read_image_file(request)
    if image is None:
        return "File is empty / Bad image"
    return str(determine_dominate_color(image))


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
    