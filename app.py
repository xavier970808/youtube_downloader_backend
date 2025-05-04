from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytubefix import YouTube
import os

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': '缺少影片連結'}), 400

        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        output_path = 'downloads'
        os.makedirs(output_path, exist_ok=True)
        filepath = stream.download(output_path=output_path)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)