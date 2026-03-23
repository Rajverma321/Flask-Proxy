from flask import Flask, Response
import requests, os

app = Flask(__name__)

@app.route('/<path:path>')
def proxy(path):
    base_url = "https://media-cdn.classplusapp.com/436362/cc/c6b3c936a0b0438ab54f008dd5d00a27-xm"
    url = f"{base_url}/{path}?key=152490450&userIds=152490450"
    r = requests.get(url, stream=True)
    return Response(r.iter_content(8192), mimetype=r.headers.get('content-type', 'video/mp2t'))

app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
