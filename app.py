from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Downloader</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:50px;">
    <h2>🎥 Multi-Site Video Downloader</h2>
    
    <form method="POST">
        <input type="text" name="url" placeholder="Paste video URL" size="50" required><br><br>
        
        <select name="quality">
            <option value="best">Best Quality</option>
            <option value="720">720p</option>
            <option value="480">480p</option>
            <option value="mp3">MP3 Audio</option>
        </select><br><br>
        
        <button type="submit">Download</button>
    </form>

    <p>{{message}}</p>
</body>
</html>
"""

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']
        
        if quality == "720":
            fmt = "bestvideo[height<=720]+bestaudio/best"
        elif quality == "480":
            fmt = "bestvideo[height<=480]+bestaudio/best"
        elif quality == "mp3":
            fmt = "bestaudio"
        else:
            fmt = "best"
        
        cmd = f'yt-dlp -f "{fmt}" -o "{DOWNLOAD_DIR}/%(title)s.%(ext)s" "{url}"'
        
        os.system(cmd)
        message = "✅ Download started! Check server files."
    
    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
