import os
from flask import Flask, request, redirect, render_template, url_for
from flask.helpers import flash
from werkzeug.utils import secure_filename

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOAD_FOLDER = ".tmp_images"
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
    return image_file


def determine_dominate_color(image_file):
    print("Good", image_file.filename)


@app.route("/api/determine_dominate_color", methods=['POST'])
def determine_dominate_color_api():
    image_file = read_image_file(request)
    if image_file is None:
        return "File is empty"
    determine_dominate_color(image_file)
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
    