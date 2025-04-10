from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = "files"

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/stream/<filename>")
def stream_file(filename):
    return render_template("stream.html", filename=filename)

@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
