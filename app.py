from flask import Flask, Response
import requests
import os

app = Flask(__name__)

def proxy_request(target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://classplusapp.com/',
        'Origin': 'https://classplusapp.com',
        'Accept': '*/*',
        'Range': 'bytes=0-'
    }
    
    r = requests.get(target_url, headers=headers, stream=True, timeout=30, allow_redirects=True)
    return r

@app.route('/')
@app.route('/master.m3u8')
def master():
    url = "https://media-cdn.classplusapp.com/436362/cc/c6b3c936a0b0438ab54f008dd5d00a27-xm/master.m3u8?key=152490450&hdnts=URLPrefix=aHR0cHM6Ly9tZWRpYS1jZG4uY2xhc3NwbHVzYXBwLmNvbS80MzYzNjIvY2Mv~Expires=1774271322~hmac=60dd0a216baf12232f33ed0acc164fcf9c9e0e0a8e39542fd192cacbc1d7edce&userIds=152490450"
    r = proxy_request(url)
    
    def generate():
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                yield chunk
    
    return Response(generate(), mimetype='application/vnd.apple.mpegurl', headers={
        'Content-Type': 'application/vnd.apple.mpegurl',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
    })

@app.route('/<path:path>')
def proxy(path):
    base_url = "https://media-cdn.classplusapp.com/436362/cc/c6b3c936a0b0438ab54f008dd5d00a27-xm"
    url = f"{base_url}/{path}?key=152490450&userIds=152490450"
    r = proxy_request(url)
    
    def generate():
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                yield chunk
    
    return Response(generate(), mimetype='video/mp2t', headers={
        'Access-Control-Allow-Origin': '*',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(len(r.content))
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)
