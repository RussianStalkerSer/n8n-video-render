from flask import Flask, request, send_file
import subprocess, tempfile, os

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/render", methods=["POST"])
def render():
    audio = request.files["audio"]

    with tempfile.TemporaryDirectory() as d:
        audio_path = os.path.join(d, "audio.mp3")
        out_path = os.path.join(d, "out.mp4")
        audio.save(audio_path)

        subprocess.run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=10",
            "-i", audio_path,
            "-shortest",
            "-movflags", "+faststart",
            out_path
        ], check=True)

        return send_file(out_path, mimetype="video/mp4")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, threaded=True)

