from flask import Flask, request, redirect, render_template
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
    filename = secure_filename(getattr(image_file, "filename", ""))
    if not(image_file and is_file_allowed(filename)):
        print("Bad input file")
        return None
    # image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = np.frombuffer(image_file.read(), np.uint8)
    image_decoded = cv2.imdecode(image, -1)
    image_decoded = cv2.cvtColor(image_decoded, cv2.COLOR_BGR2RGB)
    return image_decoded


# debug
def _calculate_mode(image):
    if len(image.shape) == 2:  # grayscale
        vals, counts = np.unique(image, return_counts=True)
        v = vals[np.argmax(counts)]
        return v

    num_channels = image.shape[-1]
    channels = np.split(image.astype(np.uint8), num_channels, axis=-1)
    merged_colors = np.zeros_like(channels[0], dtype=np.uint32)
    for ch in channels:  # rgb
        merged_colors = merged_colors << 8
        merged_colors += ch

    vals, counts = np.unique(merged_colors, return_counts=True)
    asort = np.argsort(counts)
    # print(counts[asort][::-1][:10])
    vals_sorted = vals[asort][::-1][:10]

    results = []
    for v in vals_sorted:
        result = []
        for _ in range(num_channels):  # bgr
            c = v & 0xFF
            v = v >> 8
            result.append(c)
        results.append(result[::-1])
    return np.array(results)

# debug
def _determine_dominate_color(image):
    mode = calculate_mode(image)
    res = ""
    for value in mode:
        if isinstance(value, np.uint8):
            value_str = f"({value},{value},{value})"
        else:
            value_str = ','.join(str(x) for x in value[:3])  # [:3] so the transparent result is visible
    # return f'<p style="color:rgb({value_str});">{value}</p>'
        s = f'<p style="background-color:rgb({value_str});">{value}</p>'
        res = res + s
    # return f'<p>{value}</p>'
    return res


def calculate_mode(image):
    if len(image.shape) == 2:  # grayscale
        vals, counts = np.unique(image, return_counts=True)
        v = vals[np.argmax(counts)]
        return v

    num_channels = image.shape[-1]
    channels = np.split(image.astype(np.uint8), num_channels, axis=-1)
    merged_colors = np.zeros_like(channels[0], dtype=np.uint32)
    for ch in channels:  # rgb
        merged_colors = merged_colors << 8
        merged_colors += ch
    vals, counts = np.unique(merged_colors, return_counts=True)
    v = vals[np.argmax(counts)]
    result = []
    for _ in range(num_channels):
        c = v & 0xFF
        v = v >> 8
        result.append(c)
    return np.array(result[::-1])


def determine_dominate_color(image):
    mode = calculate_mode(image)
    value = mode
    # if isinstance(value, np.uint8):
    #     value_str = f"({value},{value},{value})"
    # else:
    #     value_str = ','.join(str(x) for x in value[:3])  # [:3] so the transparent result is visible
    # return f'<p style="background-color:rgb({value_str});">{value}</p>'
    return value


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
    