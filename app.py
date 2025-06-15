from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess
import uuid
import time
from werkzeug.utils import secure_filename
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(handler)

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def async_processing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from threading import Thread
        thread = Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def cleanup_old_files(directory, max_age_hours=24):
    """Remove files older than max_age_hours"""
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = (now - os.path.getmtime(file_path)) / 3600  # hours
            if file_age > max_age_hours:
                try:
                    os.remove(file_path)
                    app.logger.info(f"Removed old file: {file_path}")
                except Exception as e:
                    app.logger.error(f"Error removing file {file_path}: {e}")

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
        # Generate unique filename to prevent collisions
        original_filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex
        file_ext = os.path.splitext(original_filename)[1]
        unique_filename = f"{unique_id}{file_ext}"
        
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        app.logger.info(f"File saved to: {filepath}")

        # Start processing in background
        process_audio(filepath, unique_id)
        
        return jsonify({
            "status": "processing",
            "task_id": unique_id,
            "message": "File is being processed"
        })
        
    except Exception as e:
        app.logger.error(f"Error during upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/status/<task_id>')
def check_status(task_id):
    """Check processing status"""
    output_folder = os.path.join(app.config['AUDIO_FOLDER'], task_id)
    
    if os.path.exists(os.path.join(output_folder, 'completed.flag')):
        return jsonify({
            "status": "completed",
            "karaoke": f"{task_id}/other.mp3",
            "autotune": f"{task_id}/vocals.mp3"
        })
    elif os.path.exists(os.path.join(output_folder, 'error.flag')):
        return jsonify({"status": "error", "message": "Processing failed"}), 500
    else:
        return jsonify({"status": "processing"})

@async_processing
def process_audio(filepath, task_id):
    """Process audio file in background"""
    try:
        output_folder = os.path.join(app.config['AUDIO_FOLDER'], task_id)
        os.makedirs(output_folder, exist_ok=True)
        
        # Create processing flag
        with open(os.path.join(output_folder, 'processing.flag'), 'w') as f:
            f.write('')
        
        # Run Demucs to separate vocals and instrumentals
        command = ["demucs", "-o", app.config['AUDIO_FOLDER'], "--filename", f"{task_id}.wav", filepath]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            app.logger.error(f"Demucs failed: {result.stderr}")
            raise Exception("Audio separation failed")
        
        # Paths to the output files
        karaoke_path = os.path.join(output_folder, "other.wav")
        autotune_path = os.path.join(output_folder, "vocals.wav")
        
        # Convert WAV to MP3 with FFmpeg
        ffmpeg_command_karaoke = [
            'ffmpeg', '-i', karaoke_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', 
            os.path.join(output_folder, "other.mp3")
        ]
        ffmpeg_command_autotune = [
            'ffmpeg', '-i', autotune_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k',
            os.path.join(output_folder, "vocals.mp3")
        ]
        
        # Run FFmpeg conversion
        for cmd in [ffmpeg_command_karaoke, ffmpeg_command_autotune]:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                app.logger.error(f"FFmpeg failed: {result.stderr}")
                raise Exception("Audio conversion failed")
        
        # Clean up temporary files
        os.remove(karaoke_path)
        os.remove(autotune_path)
        os.remove(filepath)
        
        # Create completion flag
        with open(os.path.join(output_folder, 'completed.flag'), 'w') as f:
            f.write('')
            
        app.logger.info(f"Processing completed for task: {task_id}")
        
    except Exception as e:
        app.logger.error(f"Error processing audio: {str(e)}")
        # Create error flag
        with open(os.path.join(output_folder, 'error.flag'), 'w') as f:
            f.write(str(e))
        
        # Clean up any partial files
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        directory = os.path.dirname(os.path.join(app.config['AUDIO_FOLDER'], filename))
        file = os.path.basename(filename)
        
        # Security check
        if '..' in filename or filename.startswith('/'):
            raise ValueError("Invalid filename")
            
        return send_from_directory(directory, file, as_attachment=True)
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({"error": str(e)}), 404

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    """Endpoint to clean up old files"""
    try:
        cleanup_old_files(app.config['UPLOAD_FOLDER'])
        cleanup_old_files(app.config['AUDIO_FOLDER'])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Schedule periodic cleanup
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cleanup_old_files, args=[app.config['UPLOAD_FOLDER']], trigger='interval', hours=1)
    scheduler.add_job(func=cleanup_old_files, args=[app.config['AUDIO_FOLDER']], trigger='interval', hours=1)
    scheduler.start()
    
    app.run(debug=True, host='0.0.0.0')
