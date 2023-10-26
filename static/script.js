async function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const originalImage = document.getElementById('originalImage');
    const returnedImage = document.getElementById('returnedImage');

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        // Display the selected image
        const objectURL = URL.createObjectURL(fileInput.files[0]);
        originalImage.src = objectURL;
        originalImage.style.display = 'block';

        // Send the image to the server via POST request
        try {
            const response = await fetch('generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const blob = await response.blob();
            const imageURL = URL.createObjectURL(blob);

            returnedImage.src = imageURL;
            returnedImage.style.display = 'block';
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    } else {
        alert('Please select an image to upload.');
    }
}
