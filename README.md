<img width="1280" alt="readme-banner" src="https://github.com/user-attachments/assets/35332e92-44cb-425b-9dff-27bcf1023c6c">

# Spoofy - Karaoke/Autotune Creator 🎯


## Basic Details
### Team Name: Harmony Forge


### Team Members
- Team Lead: Aldrin Abraham - SSET

### Project Description
Spoofy is a web platform that transforms uploaded songs into karaoke and autotune versions using AI-powered audio separation with Demucs. Users can upload a song and instantly receive high-quality, isolated vocal and instrumental tracks, perfect for karaoke enthusiasts and remix creators. Built for seamless audio processing, Spoofy brings professional-grade music tools to everyone.

### The Problem (that doesn't exist)
In today’s digital age, music creators and enthusiasts often seek ways to experiment with and customize their favorite tracks, whether for karaoke sessions, remixing, or personal projects. However, achieving high-quality separation of vocals and instrumentals from a song often requires specialized audio processing software and technical expertise, which can be complex and inaccessible to casual users.

Challenges include:
* Limited Accessibility: Most audio separation tools are complex and require knowledge of audio engineering or technical skills to operate.
* High Costs: Professional-grade tools for audio separation are often costly and inaccessible to average users.
* Lack of Automation: For non-technical users, the steps involved in manually isolating vocals and instruments can be tedious and time-consuming.

### The Solution (that nobody asked for)
Spoofy addresses these challenges by providing an intuitive, web-based platform that automates the process of separating a song into karaoke (instrumental) and autotune (vocal) versions using AI-powered Demucs technology. With a simple upload process, Spoofy enables users to instantly access instrumental and vocal tracks, empowering them to create karaoke sessions, remixes, or custom audio projects with ease. This makes audio processing technology accessible, affordable, and user-friendly for a wider audience.

## Technical Details
### Technologies/Components Used
For Software:

1. Languages Used:
* Python: Backend development, handling file uploads, and processing using the Demucs model.
* HTML/CSS: For building the frontend structure and styling.
* JavaScript: For dynamic frontend interactions like progress bars and handling file uploads.

2. Frameworks Used:
* Flask: A lightweight web framework for routing, managing user requests, and serving the web application.

3. Libraries Used:
* Demucs: For audio source separation (splits audio into vocals and instrumentals).
* Torch: Required as the underlying library for Demucs, providing model processing capabilities.
* Werkzeug: A Python library used by Flask for secure file handling.

4. Tools Used:
* VS Code: For code editing and debugging.
* Git: Version control for managing changes and collaboration.
* GitHub: For hosting and managing the project repository.

For Hardware:

1. Main Components:
* Computer: General-purpose computer or laptop capable of running Python and Flask applications.
* Speakers: For testing audio output of processed tracks.

2. Specifications:
* Processor: Intel i5 or equivalent recommended for local processing.
* RAM: Minimum 8GB to handle audio processing tasks smoothly.
* Storage: Sufficient disk space to handle multiple audio files (at least 1 GB free).

3. Tools Required:
* Python Environment: Python 3.x installed on the system.
* Package Manager: pip for managing and installing dependencies.

### Implementation
For Software:

1. File Upload and Server Setup:
* Flask handles incoming file uploads from the frontend.
* Uploaded files are stored temporarily in the uploads/ directory, with the file paths referenced for processing.

2. Audio Processing Using Demucs:
* The uploaded audio file is processed using Demucs.
* Demucs model loads the file and splits it into two outputs:
* Instrumental (Karaoke) Track: Extracted from the audio as an isolated instrumental.
* Vocal (Autotune) Track: Isolated vocal track generated separately.
* Processed audio files are saved in static/audio/ for easy access from the web interface.

3. Frontend Design and User Interaction:
* The index.html page includes a file upload form, with JavaScript functions to display progress bars during the upload and processing stages.
* JavaScript (script.js) dynamically updates progress bars to reflect upload and processing status.
* CSS (style.css) provides styling to center elements and enhance the visual layout of the progress bars and download links.

4. Downloadable Output:
* Processed files (instrumental and vocal tracks) are made available for download once processing completes.
* Links to these files are dynamically generated and displayed on the frontend.

# Installation
1. Clone the repository:
~~~bash
git clone https://github.com/yourusername/spoofy-origin.git
cd spoofy-origin
~~~

2. Set up a virtual environment (optional but recommended):
~~~bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
~~~

3. Install dependencies:
~~~bash
pip install -r requirements.txt
~~~

# Run
1.Start the Flask server:
~~~bash
python app.py
~~~
2.Open your browser and go to:
~~~arduino
http://localhost:5000
~~~
3.Upload a song, and the progress bar will display upload and processing stages. After completion, download options for karaoke and autotune versions will appear.

### Project Documentation
For Software:
#### Overview
Spoofy Origin is a web-based application that takes any song as input, processes it to separate the instrumental (karaoke) and vocal (autotune) tracks using machine learning and audio processing techniques with the Demucs library. Users can download the karaoke and autotune versions of their uploaded track for creative uses like singing along or remixing.

#### Features
* Song Upload: Users can upload any supported audio file (e.g., MP3).
* Audio Separation: Demucs processes the song to split it into isolated vocal and instrumental tracks.
* Download Options: Users can download either the karaoke (instrumental) or autotune (vocal) version of the song.
* Real-time Progress Feedback: Progress bars show upload and processing statuses.

#### Technologies Used
* Languages: Python, JavaScript, HTML, CSS
* Frameworks: Flask (for backend and server handling)
* Libraries:
  * Demucs: For machine learning-based audio source separation
  * Flask: To build the web server and handle user requests
  * Jinja2: Flask’s templating engine for rendering dynamic HTML
* Tools:
  * ffmpeg: Necessary for audio processing by Demucs
  * Virtualenv: For creating isolated environments (optional but recommended)

#### Architecture
The project uses a client-server architecture with the following components:

* Frontend (HTML/CSS/JavaScript):
User interface for uploading files, displaying progress, and providing download options.
JavaScript manages the progress bar and handles async communication with the backend.

* Backend (Python/Flask):
Routes for handling file uploads, audio processing, and generating output download links.
Uses Demucs for processing and separating audio tracks, with Flask managing the workflow and file handling.

# Screenshots
1. Webpage before uploading

![1](https://github.com/user-attachments/assets/d1accde9-e9a3-48e9-aedf-d66c3db8a2f8)


2. Webpage during processing

![2](https://github.com/user-attachments/assets/9cbf3da9-a13b-4ab1-9636-b1710fa409f1)


3. Webpage after processing

![3](https://github.com/user-attachments/assets/49e2be86-5810-4e7b-9b1a-3bf105b5dea5)

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProject--24-24?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)

---
# Version 2

Spoofy v1 was a foundational prototype that focused solely on backend audio separation using Demucs. While it successfully extracted four audio stems (bass, drums, vocals, other), users had no way to interact with or download these files via a web interface.

Spoofy v2, the current version, is a fully functional upgrade with:
* A complete frontend UI for uploading songs, visualizing progress, and downloading results.
* Conversion of .wav files to .mp3 for easy playback and sharing.
* Downloadable karaoke (other) and autotuned vocals directly from the browser.
* Task-based async handling and auto-cleanup of old files.
 
While v2 still excludes bass and drums from the karaoke track and offers basic audio quality, it marks a significant leap from raw processing to an interactive user experience.

# 🎧 Spoofy – AI Music Splitter & Autotuner

Spoofy is a full-stack web app that lets users upload a song and receive two downloadable versions: a karaoke-style instrumental (without vocals) and an autotuned vocal track. Powered by Demucs for source separation and FFmpeg for conversion, Spoofy features:
* A smooth, drag-and-drop interface with real-time progress feedback.
* Auto-conversion and download of audio without needing manual file handling.
* Background processing and task status polling to ensure non-blocking UX.

While not professional studio-grade, Spoofy offers a fast and easy way to separate and enhance vocals for casual remixing, practice, or fun.

# 🔧 Technical Details
## ✅ Technologies / Components Used

### 🖥️ For Software:

Languages Used:
* Python: Backend logic, audio processing using Demucs, and handling file uploads.
* HTML / CSS: Structuring and styling the frontend interface.
* JavaScript: For dynamic frontend interaction including drag-and-drop, progress updates, and file handling.

Frameworks Used:
* Flask: Lightweight Python web framework used for routing, server setup, and serving HTML templates.

Libraries Used:
* Demucs: Deep learning model for music source separation.
* Torch: Underlying machine learning framework required by Demucs.
* Werkzeug: Flask’s internal library for secure filename handling.

Tools Used:
* VS Code: Code editor used for development.
* Git: Version control system for managing source code.
* GitHub: Repository hosting and version tracking.

### 🖥️ For Hardware:

Main Components:
* A general-purpose computer/laptop capable of running Python and Flask.

Specifications Recommended:
* Processor: Intel i5 or equivalent.
* RAM: Minimum 8GB for smooth audio processing.
* Storage: At least 1GB free for temporary audio files.
* Speakers: For playback and testing of processed audio.

Tools Required:
* Python 3.x: Installed environment for running the project.
* pip: Python package manager for dependency installation.

## ⚙️ Implementation

### 🗃️ File Upload & Server Setup:
* Users upload an audio file via the web interface.
* Flask handles the request and stores the file temporarily in /uploads.
* Files are assigned unique IDs using UUID to avoid overwriting.

### 🎛️ Audio Processing Using Demucs:
* Flask calls Demucs to split the uploaded song into four parts (vocals, bass, drums, other).
* Only the vocals and other are kept.
  * Vocals are processed into the autotune version.
  * Other (without vocals, bass, and drums) becomes the karaoke version.
* Output files are saved in static/audio/<task_id>/.

### 🎨 Frontend Design & User Interaction:
* index.html provides a responsive UI for file upload.
* Progress updates (upload & processing) are displayed in real-time using JavaScript (script.js).
* Styles are defined in style.css, offering a clean and modern aesthetic.

### 💾 Downloadable Output:
* When processing is complete, download links are generated dynamically using the task_id.
* The user can preview or download the karaoke and autotune MP3 files.

## 🛠️ Installation

### 📥 Clone the Repository:
~~~bash
git clone https://github.com/yourusername/spoofy-origin.git
cd spoofy-origin
~~~

### 🧪 Set Up Virtual Environment (Optional but Recommended):
~~~bash
python -m venv venv
# Activate:
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
~~~

### 📦 Install Dependencies:
~~~bash
pip install -r requirements.txt
~~~

## ▶️ Run the Project

1. Start the Flask server:
~~~bash
python app.py
~~~

2. Open your browser and go to:
~~~bash
http://localhost:5000
~~~

3. Upload an audio file. Once processed, download links for karaoke and autotune versions will appear.

## 📄 Project Documentation

### 📌 Overview:
Spoofy Origin is a web-based audio processing tool that uses AI-powered source separation to extract vocals and instrumentals from user-uploaded songs. It allows users to download karaoke (instrumental) and autotune (vocal) versions for creative uses such as covers, remixing, or practice.

✨ Features:
* 🎵 Song Upload: Drag-and-drop interface for user-friendly uploads.
* 🧠 Audio Separation: Uses machine learning to isolate vocals and music.
* 📥 Download Options: Output files available directly in MP3 format.
* 📊 Live Progress Bar: Visual feedback during processing.
* 🔄 Reset & Reupload: Simple interface to process multiple songs.

🧱 Technologies Used:
* Languages: Python, JavaScript, HTML, CSS
* Framework: Flask
* Libraries: Demucs, Torch, Flask, Werkzeug
* Tools: FFmpeg (for audio conversion), Virtualenv (optional environment)

## 🏗️ Architecture

### 🔁 Client-Server Model:

Frontend (HTML/CSS/JavaScript):
* Handles user uploads, progress display, and download actions.
* Interacts with backend via fetch for upload and task status polling.

Backend (Python + Flask):
* Manages file uploads, stores files, and triggers processing.
* Runs Demucs + FFmpeg to produce output.
* Serves completed files through Flask endpoints (/download/<file>).

# Screenshots
1. Webpage before uploading

![Start](https://github.com/user-attachments/assets/99e8c911-11db-400e-ad7f-e2bdf5376ded)

2. Webpage during processing

![Middle](https://github.com/user-attachments/assets/fdc148a1-4bdb-4718-947a-8ec11e673269)

3. Webpage after processing

![End](https://github.com/user-attachments/assets/7a78e13c-7129-4a62-aea2-cd4ca8813f0f)

---
