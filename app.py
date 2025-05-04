from flask import Flask, request, send_file, jsonify
from pytubefix import YouTube
from pytubefix.cli import on_progress
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

app.config['DOWNLOAD_FOLDER'] = 'downloads'
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'Missing URL'}), 400

        uid = str(uuid.uuid4())[:8]
        folder = os.path.join(app.config['DOWNLOAD_FOLDER'], uid)
        os.makedirs(folder)

        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        filepath = stream.download(output_path=folder)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)