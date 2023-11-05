# Import required libraries
import io
import logging
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener

# Enable heic files to be opened
register_heif_opener()

def file_size(buf):
    """
    This function gets the size of a buffer.
    
    Inputs
    -----------
    buf : bytes.io
        Array of bytes
    
    Output
    ----------
    size : int
        Returns length of buffer in bytes
    """
    file_pos = buf.tell()
    buf.seek(0, io.SEEK_END)
    size = buf.tell()
    buf.seek(file_pos)
    return size


def human_readable_size(size, decimal_places=2):
    """
    This function takes a size in bytes and converts it into a 
    human-readable string with units.

    Inputs
    ---------
    size : int
        Number of bytes
    
    decimal_places : int
        Number of decimal places to display
    
    Outputs
    ---------
    Formatted string
    """
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def histogram(img):
    """
    This function returns a figure containing a histogram plot.

    Inputs
    --------
    img : bytes.io
        Raw image
    
    Outputs
    --------
    fig : matplotlib figure
        Contains image histogram plot
    """
    logging.info(f"Image size:   {human_readable_size(file_size(img))}")
    image = Image.open(img)

    logging.info(f"Image format: {image.format}")
    logging.info(f"Image mode:   {image.mode}")
    logging.info(f"Image size:   {image.size} px")

    # Raise error if image is not RGB or RGBA type
    if image.mode != "RGB" and image.mode != "RGBA":
        raise ValueError("Image mode must be RGB or RGBA")

    # Get Numpy array of RGB values
    np_array = np.array(image)

    # Get the histogram for each channel
    channel_histograms = compute_single_channel_histograms(np_array)

    # Setup matplotlib figure
    fig, ax = plt.subplots(1, 1)

    # Plot the histogram for each channel
    # * unpacks tuple into separate arguments
    ax.stairs(*channel_histograms[0], label="Red", color="red")
    ax.stairs(*channel_histograms[1], label="Green", color="green")
    ax.stairs(*channel_histograms[2], label="Blue", color="blue")
    ax.set_title("Histogram")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Count")
    ax.legend()

    return fig


def compute_single_channel_histograms(img, bins=256, range=(0, 256)):
    """
    This function returns histograms for each channel of an image.

    Inputs 
    --------
    img : numpy array
        Numpy array representing multi-channel image
    
    bins : int (default=256)
        Number of bins to use in the histogram plot
    
    range : tuple (default (0, 256))
        Defines range of the bins
    
    Output
    --------
    A list of histograms; each histogram is a tuple containing the bin boundaries 
    and the bin frequencies.
    """
    num_channels = img.shape[2]
    channels = np.array_split(img, num_channels, axis=2)

    # Remove the singleton dimension
    channels = map(lambda x: np.squeeze(x), channels)

    # Compute the histogram for each channel
    return list(map(lambda x: np.histogram(x, bins=bins, range=range), channels))


# Use for local testing
if __name__ == "__main__":
    # If using - update image path!
    with open("imgs/IMG_3946.jpeg", "rb") as f:
        histogram(f)
        plt.show()
