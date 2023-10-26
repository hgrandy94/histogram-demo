import io
from logging.config import dictConfig

from flask import Flask
from flask import request
from flask import send_file

import matplotlib.pyplot as plt

from histogram import histogram

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
)


app = Flask(
    __name__,
    static_folder="static",
)

# Make sure we use the Agg backend for matplotlib
plt.switch_backend("Agg")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    # Load the image from the request body
    image = request.files["image"]

    # Generate the histogram
    histogram_fig = histogram(image)

    # Save the figure to a bytes object
    bytes_obj = io.BytesIO()
    histogram_fig.savefig(bytes_obj, format="png")
    bytes_obj.seek(0)

    # Return the bytes object
    return send_file(bytes_obj, mimetype="image/png")
