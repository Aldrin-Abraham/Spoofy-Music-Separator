function uploadSong() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const downloadLinks = document.getElementById('download-links');

    progressContainer.style.display = 'block';

    // Start the simulated progress
    let simulatedProgress = 0;
    const interval = setInterval(() => {
        if (simulatedProgress < 95) {
            simulatedProgress += 0.35; // Increment by 0.35% every 1000ms
            progressBar.value = simulatedProgress;
            progressText.textContent = simulatedProgress + '%';
        } else {
            clearInterval(interval); // Stop simulating progress when reaching 95%
        }
    }, 1000); // Update every 1000ms

    // Create a new XMLHttpRequest for the actual upload
    const xhr = new XMLHttpRequest();

    // Update the progress bar during the actual upload
    xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable) {
            const percentComplete = (event.loaded / event.total) * 100;
            // This ensures that the bar only reaches 95% while uploading
            progressBar.value = Math.min(95, percentComplete);
            progressText.textContent = Math.round(progressBar.value) + '%';
        }
    });

    // Handle the response
    xhr.onload = () => {
        clearInterval(interval); // Clear the interval once upload completes
        progressBar.value = 100; // Set progress to 100%
        progressText.textContent = 'Upload complete!';

        const data = JSON.parse(xhr.responseText);
        // Display download links
        downloadLinks.style.display = 'block';
        document.getElementById('karaoke-link').href = `/download/${data.karaoke}`;
        document.getElementById('autotune-link').href = `/download/${data.autotune}`;
    };

    // Handle errors
    xhr.onerror = () => {
        clearInterval(interval); // Clear the interval on error
        console.error('Upload failed.');
    };

    // Start the actual upload
    xhr.open('POST', '/upload');
    xhr.send(formData);
}
