from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Run Demucs to separate vocals and instrumentals
        command = ["demucs", "-o", app.config['AUDIO_FOLDER'], filepath]
        subprocess.run(command)

        # Paths to the output files
        karaoke_path = os.path.join(app.config['AUDIO_FOLDER'], file.filename.replace(".mp3", ""), "no_vocals.wav")
        autotune_path = os.path.join(app.config['AUDIO_FOLDER'], file.filename.replace(".mp3", ""), "vocals.wav")

        return jsonify({
            "karaoke": karaoke_path,
            "autotune": autotune_path
        })
    return jsonify({"error": "No file provided"}), 400

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
