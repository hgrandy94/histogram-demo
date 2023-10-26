import io
import logging

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()


def file_size(buf):
    file_pos = buf.tell()
    buf.seek(0, io.SEEK_END)
    size = buf.tell()
    buf.seek(file_pos)
    return size


def human_readable_size(size, decimal_places=2):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def histogram(img):
    logging.info(f"Image size:   {human_readable_size(file_size(img))}")
    image = Image.open(img)

    logging.info(f"Image format: {image.format}")
    logging.info(f"Image mode:   {image.mode}")
    logging.info(f"Image size:   {image.size} px")

    print(f"Image format: {image.format}")
    print(f"Image mode:   {image.mode}")
    print(f"Image size:   {image.size} px")

    if image.mode != "RGB" and image.mode != "RGBA":
        raise ValueError("Image mode must be RGB or RGBA")

    # Get Numpy array of RGB values
    np_array = np.array(image)
    #print(np_array.shape)

    # Get the histogram for each channel
    channel_histograms = compute_single_channel_histograms(np_array)

    fig, ax = plt.subplots(1, 1)

    # Plot the histogram for each channel
    ax.stairs(*channel_histograms[0], label="Red", color="red")
    ax.stairs(*channel_histograms[1], label="Green", color="green")
    ax.stairs(*channel_histograms[2], label="Blue", color="blue")

    ax.set_title("Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Count")
    ax.legend()

    return fig


def compute_single_channel_histograms(img, bins=256, range=(0, 256)):
    num_channels = img.shape[2]
    channels = np.array_split(img, num_channels, axis=2)

    # Remove the singleton dimension
    channels = map(lambda x: np.squeeze(x), channels)

    # Compute the histogram for each channel
    return list(map(lambda x: np.histogram(x, bins=bins, range=range), channels))


if __name__ == "__main__":
    with open("imgs/IMG_3946.jpeg", "rb") as f:
        histogram(f)
        plt.show()
