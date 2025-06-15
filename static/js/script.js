document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('upload-btn');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    const progressStatus = document.getElementById('progress-status');
    const timeEstimate = document.getElementById('time-estimate');
    const resultsContainer = document.getElementById('results-container');
    const fileNameDisplay = document.getElementById('file-name');
    const resetBtn = document.getElementById('reset-btn');
    const audioPreview = document.getElementById('audio-preview');
    const playerModal = document.getElementById('player-modal');
    const closeModalBtn = document.querySelector('.close-modal');
    const karaokeCard = document.getElementById('karaoke-card');
    const autotuneCard = document.getElementById('autotune-card');

    // State variables
    let currentTaskId = null;
    let progressInterval = null;
    let uploadStartTime = null;
    const processingSteps = [
        "Uploading file...",
        "Analyzing audio...",
        "Separating vocals from instrumental...",
        "Applying autotune effects...",
        "Finalizing tracks...",
        "Processing complete!"
    ];

    // Initialize event listeners
    setupEventListeners();

    function setupEventListeners() {
        fileInput.addEventListener('change', handleFileSelect);
        
        uploadForm.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadForm.classList.add('dragover');
        });
        
        uploadForm.addEventListener('dragleave', () => {
            uploadForm.classList.remove('dragover');
        });
        
        uploadForm.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadForm.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        });
        
        uploadBtn.addEventListener('click', uploadSong);
        resetBtn.addEventListener('click', resetForm);
        
        closeModalBtn.addEventListener('click', closeModal);
        document.getElementById('play-selected').addEventListener('click', playSelectedPreview);
        document.getElementById('close-player').addEventListener('click', closeModal);
        
        document.getElementById('share-btn').addEventListener('click', shareResults);
    }

    function handleFileSelect() {
        const file = fileInput.files[0];
        if (!file) return;
        
        if (!validateFile(file)) {
            return;
        }
        
        fileNameDisplay.textContent = file.name;
        uploadBtn.disabled = false;
        
        // Create preview URL for audio
        const previewURL = URL.createObjectURL(file);
        audioPreview.src = previewURL;
    }

    function validateFile(file) {
        const validTypes = ['audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/flac', 'audio/ogg', 'audio/m4a'];
        const maxSize = 50 * 1024 * 1024; // 50MB
        
        if (!validTypes.includes(file.type)) {
            showError('Invalid file type. Please upload MP3, WAV, FLAC, OGG, or M4A files.');
            return false;
        }
        
        if (file.size > maxSize) {
            showError('File too large. Maximum size is 50MB.');
            return false;
        }
        
        return true;
    }

    function showError(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        uploadForm.appendChild(errorElement);
        uploadBtn.disabled = true;
    }

    async function uploadSong() {
        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file first');
            return;
        }
        
        uploadBtn.disabled = true;
        progressContainer.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        
        const formData = new FormData();
        formData.append('file', file);
        
        startProgressSimulation();
        uploadStartTime = Date.now();
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }
            
            const data = await response.json();
            currentTaskId = data.task_id;
            checkProcessingStatus();
        } catch (error) {
            handleUploadError(error);
        }
    }

    function startProgressSimulation() {
        let simulatedProgress = 0;
        let currentStep = 0;
        
        progressInterval = setInterval(() => {
            if (simulatedProgress < 80) {
                simulatedProgress += Math.random() * 3;
                progressBar.value = simulatedProgress;
                progressPercent.textContent = `${Math.round(simulatedProgress)}%`;
                
                if (simulatedProgress > currentStep * 15 && currentStep < processingSteps.length - 1) {
                    currentStep++;
                    progressStatus.textContent = processingSteps[currentStep];
                }
                
                updateTimeEstimate(simulatedProgress);
            }
        }, 800);
    }

    function updateTimeEstimate(progress) {
        if (!uploadStartTime || progress <= 0) return;
        
        const elapsed = (Date.now() - uploadStartTime) / 1000;
        const estimatedTotal = (elapsed / progress) * 100;
        const remaining = Math.max(0, estimatedTotal - elapsed);
        
        if (remaining > 60) {
            timeEstimate.textContent = `Estimated time remaining: ${Math.round(remaining / 60)} minutes`;
        } else {
            timeEstimate.textContent = `Estimated time remaining: ${Math.round(remaining)} seconds`;
        }
    }

    async function checkProcessingStatus() {
        if (!currentTaskId) return;
        
        try {
            const response = await fetch(`/status/${currentTaskId}`);
            const data = await response.json();
            
            if (data.status === 'completed') {
                clearInterval(progressInterval);
                handleUploadSuccess(data);
            } else if (data.status === 'error') {
                clearInterval(progressInterval);
                handleUploadError(new Error(data.message || 'Processing failed'));
            } else {
                setTimeout(checkProcessingStatus, 2000);
            }
        } catch (error) {
            console.error('Error checking status:', error);
            setTimeout(checkProcessingStatus, 2000);
        }
    }

    function handleUploadSuccess(data) {
        progressBar.value = 100;
        progressPercent.textContent = '100%';
        progressStatus.textContent = 'Processing complete!';
        timeEstimate.textContent = 'Ready to download your files';
        
        setTimeout(() => {
            progressContainer.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
            
            document.getElementById('karaoke-link').href = `/download/${data.karaoke}`;
            document.getElementById('autotune-link').href = `/download/${data.autotune}`;
            
            karaokeCard.onclick = () => previewTrack(data.karaoke);
            autotuneCard.onclick = () => previewTrack(data.autotune);
        }, 1000);
    }

    function handleUploadError(error) {
        console.error('Upload failed:', error);
        progressStatus.textContent = 'Error processing file';
        progressStatus.style.color = 'var(--error-color)';
        timeEstimate.textContent = 'Please try again';
        
        setTimeout(() => {
            resetForm();
        }, 3000);
    }

    function previewTrack(trackPath) {
        audioPreview.src = `/download/${trackPath}`;
        playerModal.classList.remove('hidden');
    }

    function playSelectedPreview() {
        audioPreview.play();
    }

    function closeModal() {
        playerModal.classList.add('hidden');
        audioPreview.pause();
    }

    function shareResults() {
        if (navigator.share) {
            navigator.share({
                title: 'Check out my Spoofy Origin tracks',
                text: 'I just created karaoke and autotune versions of my song!',
                url: window.location.href,
            }).catch(err => {
                console.log('Error sharing:', err);
                copyToClipboard();
            });
        } else {
            copyToClipboard();
        }
    }

    function copyToClipboard() {
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            alert('Link copied to clipboard!');
        });
    }

    function resetForm() {
        fileInput.value = '';
        fileNameDisplay.textContent = 'Choose an audio file or drag it here';
        uploadBtn.disabled = false;
        progressContainer.classList.add('hidden');
        resultsContainer.classList.add('hidden');
        playerModal.classList.add('hidden');
        
        progressBar.value = 0;
        progressPercent.textContent = '0%';
        progressStatus.textContent = processingSteps[0];
        progressStatus.style.color = '';
        timeEstimate.textContent = 'Estimated time remaining: calculating...';
        
        const errorElement = document.querySelector('.error-message');
        if (errorElement) {
            errorElement.remove();
        }
        
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
        
        currentTaskId = null;
        audioPreview.pause();
        audioPreview.src = '';
    }
});
