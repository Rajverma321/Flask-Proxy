from flask import Flask, Response
import requests, os

app = Flask(__name__)

@app.route('/')
@app.route('/master.m3u8')
def master():
    url = "https://media-cdn.classplusapp.com/436362/cc/c6b3c936a0b0438ab54f008dd5d00a27-xm/master.m3u8?key=152490450&userIds=152490450"
    r = requests.get(url, stream=True)
    return Response(r.iter_content(8192), mimetype='application/vnd.apple.mpegurl')

@app.route('/<path:path>')
def proxy(path):
    base_url = "https://media-cdn.classplusapp.com/436362/cc/c6b3c936a0b0438ab54f008dd5d00a27-xm"
    url = f"{base_url}/{path}?key=152490450&userIds=152490450"
    r = requests.get(url, stream=True)
    return Response(r.iter_content(8192), mimetype='video/mp2t')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
