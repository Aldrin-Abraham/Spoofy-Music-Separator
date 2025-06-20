from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import uuid
import time
import logging
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(handler)

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def normalize_path(*paths):
    """Convert paths to absolute and normalize slashes for Windows"""
    return os.path.abspath(os.path.join(*paths))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    try:
        # Generate unique filename
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(secure_filename(file.filename))[1]
        unique_filename = f"{unique_id}{file_ext}"
        filepath = normalize_path(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        app.logger.info(f"File saved to: {filepath}")

        # Start processing
        process_audio(filepath, unique_id)
        
        return jsonify({
            "status": "processing",
            "task_id": unique_id,
            "message": "File is being processed"
        })
        
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def process_audio(filepath, task_id):
    """Background audio processing"""
    try:
        output_folder = normalize_path(app.config['AUDIO_FOLDER'], task_id)
        os.makedirs(output_folder, exist_ok=True)
        
        # Run Demucs (with explicit model to ensure consistent output paths)
        demucs_output = normalize_path(output_folder, "htdemucs")
        command = [
            "demucs",
            "--name", "htdemucs",
            "-o", output_folder,
            filepath
        ]
        
        app.logger.info(f"Running Demucs: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, timeout=600)  # 10min timeout
        
        if result.returncode != 0:
            raise Exception(f"Demucs failed: {result.stderr}")
        
        # Verify outputs
        separated_folder = normalize_path(demucs_output, os.path.basename(filepath).rsplit('.', 1)[0])
        karaoke_wav = normalize_path(separated_folder, "other.wav")
        vocals_wav = normalize_path(separated_folder, "vocals.wav")
        
        if not os.path.exists(karaoke_wav):
            raise FileNotFoundError(f"Demucs output missing: {karaoke_wav}")
        
        # Convert to MP3
        karaoke_mp3 = normalize_path(output_folder, "other.mp3")
        vocals_mp3 = normalize_path(output_folder, "vocals.mp3")
        
        if not convert_to_mp3(karaoke_wav, karaoke_mp3):
            raise Exception("Karaoke conversion failed")
        if not convert_to_mp3(vocals_wav, vocals_mp3):
            raise Exception("Vocals conversion failed")
        
        # Cleanup temporary files
        os.remove(filepath)
        os.remove(karaoke_wav)
        os.remove(vocals_wav)
        
        # Create completion flag
        with open(normalize_path(output_folder, "completed.flag"), 'w') as f:
            f.write('')
            
        app.logger.info(f"Processing completed for {task_id}")
        
    except Exception as e:
        app.logger.error(f"Processing error: {str(e)}")
        error_flag = normalize_path(output_folder, "error.flag")
        with open(error_flag, 'w') as f:
            f.write(str(e))
        
        # Cleanup partial files
        if os.path.exists(filepath):
            os.remove(filepath)

def convert_to_mp3(input_path, output_path):
    """Convert WAV to MP3 using FFmpeg"""
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
        output_path
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            app.logger.error(f"FFmpeg failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        app.logger.error(f"FFmpeg exception: {str(e)}")
        return False

@app.route('/status/<task_id>')
def check_status(task_id):
    output_folder = normalize_path(app.config['AUDIO_FOLDER'], task_id)
    
    if os.path.exists(normalize_path(output_folder, "error.flag")):
        with open(normalize_path(output_folder, "error.flag"), 'r') as f:
            return jsonify({"status": "error", "message": f.read()}), 500
            
    if os.path.exists(normalize_path(output_folder, "completed.flag")):
        return jsonify({
            "status": "completed",
            "karaoke": f"{task_id}/other.mp3",
            "autotune": f"{task_id}/vocals.mp3"
        })
    
    return jsonify({"status": "processing"})

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        directory = os.path.dirname(normalize_path(app.config['AUDIO_FOLDER'], filename))
        file = os.path.basename(filename)
        
        if '..' in filename or not os.path.exists(normalize_path(directory, file)):
            raise ValueError("Invalid filename")
            
        return send_from_directory(directory, file, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({"error": str(e)}), 404

def cleanup_old_files():
    """Delete files older than 24 hours"""
    now = time.time()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['AUDIO_FOLDER']]:
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                file_age = (now - os.path.getmtime(filepath)) / 3600
                if file_age > 24:
                    try:
                        os.remove(filepath)
                        app.logger.info(f"Cleaned up: {filepath}")
                    except Exception as e:
                        app.logger.error(f"Cleanup failed: {filepath} - {str(e)}")

if __name__ == '__main__':
    # Schedule cleanup every hour
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_old_files, 'interval', hours=1)
    scheduler.start()
    
    app.run(debug=True, host='0.0.0.0')
