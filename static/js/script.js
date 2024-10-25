function uploadSong() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const downloadLinks = document.getElementById('download-links');

    progressContainer.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        progressText.textContent = '100%';
        progressBar.value = 100;

        // Display download links
        downloadLinks.style.display = 'block';
        document.getElementById('karaoke-link').href = `/download/${data.karaoke}`;
        document.getElementById('autotune-link').href = `/download/${data.autotune}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
