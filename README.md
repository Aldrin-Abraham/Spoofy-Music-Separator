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
***bash
Copy code
git clone https://github.com/yourusername/spoofy-origin.git
cd spoofy-origin

2. Set up a virtual environment (optional but recommended):
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

3. Install dependencies:
bash
Copy code
pip install -r requirements.txt

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProject--24-24?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)
