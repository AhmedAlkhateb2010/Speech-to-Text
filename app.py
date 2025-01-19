from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import time
from process import process_audio_to_excel

app = Flask(__name__)

# Configure upload and output folders
app.config['UPLOAD_FOLDER'] = r'C:\Users\Msi\Desktop\Speech to Text\uploads'
app.config['EXCEL_FOLDER'] = r'C:\Users\Msi\Desktop\Speech to Text\output'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac', 'm4a', 'ogg'}

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXCEL_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """
    Render the home page with the upload form.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return jsonify({"message": "File uploaded successfully.", "file_path": file_path}), 200
    else:
        return jsonify({"error": "Invalid file format. Allowed formats: mp3, wav, flac, m4a, ogg."}), 400


@app.route('/upload-and-convert', methods=['POST'])
def upload_and_convert():
    """
    Handle file upload and conversion to Excel.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading."}), 400

    if file and allowed_file(file.filename):
        start_time = time.time()

        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the audio file and generate Excel
        try:
            excel_path = process_audio_to_excel(file_path, app.config['EXCEL_FOLDER'])
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500

        processing_time = round(time.time() - start_time, 2)

        return jsonify({
            "download_url": f"/download/{os.path.basename(excel_path)}",
            "processing_time": processing_time
        }), 200
    else:
        return jsonify({"error": "Invalid file format. Allowed formats: mp3, wav, flac, m4a, ogg."}), 400


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Handle downloading of the generated Excel file.
    """
    file_path = os.path.join(app.config['EXCEL_FOLDER'], filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found."}), 404

    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
