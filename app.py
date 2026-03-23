from flask import Flask, request, render_template_string, jsonify
import subprocess
import threading
import re

app = Flask(__name__)

progress_data = {
    "percent": "0%",
    "speed": "0 MB/s",
    "status": "Idle"
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Pro Downloader</title>
    <style>
        body { background:#0f172a; color:white; text-align:center; font-family:Arial; }
        .box { background:#1e293b; padding:20px; margin:auto; width:400px; border-radius:10px; }
        input, select, button { padding:10px; margin:10px; }
        .bar { width:100%; background:#334155; height:20px; border-radius:10px; }
        .fill { height:100%; width:0%; background:#22c55e; border-radius:10px; }
    </style>
</head>
<body>

<div class="box">
    <h2>🚀 Video Downloader</h2>

    <form method="POST">
        <input type="text" name="url" placeholder="Paste URL" required><br>
        <select name="quality">
            <option value="best">Best</option>
            <option value="720">720p</option>
            <option value="480">480p</option>
            <option value="mp3">MP3</option>
        </select><br>
        <button type="submit">Download</button>
    </form>

    <h3>Status: <span id="status">Idle</span></h3>
    <div class="bar"><div class="fill" id="bar"></div></div>
    <p id="percent">0%</p>
    <p id="speed">0 MB/s</p>
</div>

<script>
setInterval(()=>{
    fetch('/progress')
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("bar").style.width = data.percent;
        document.getElementById("percent").innerText = data.percent;
        document.getElementById("speed").innerText = data.speed;
        document.getElementById("status").innerText = data.status;
    });
},1000);
</script>

</body>
</html>
"""

def download_thread(url, fmt):
    global progress_data
    progress_data["status"] = "Downloading..."

    cmd = f'yt-dlp -f "{fmt}" "{url}"'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        match = re.search(r'(\\d+\\.\\d+)%.*?(\\d+\\.\\d+MiB/s)', line)
        if match:
            progress_data["percent"] = match.group(1) + "%"
            progress_data["speed"] = match.group(2)

    progress_data["status"] = "Completed"

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        q = request.form["quality"]

        if q == "720":
            fmt = "bestvideo[height<=720]+bestaudio"
        elif q == "480":
            fmt = "bestvideo[height<=480]+bestaudio"
        elif q == "mp3":
            fmt = "bestaudio"
        else:
            fmt = "best"

        threading.Thread(target=download_thread, args=(url, fmt)).start()

    return render_template_string(HTML)

@app.route("/progress")
def progress():
    return jsonify(progress_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
