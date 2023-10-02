from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

@app.route('/', methods=['GET', 'POST'])
def proxy_api():
    url = request.args.get('url')
    if not url:
        return jsonify(error='Missing url query parameter'), 400

    try:
        if request.method == 'GET':
            response = requests.get(url, params=request.args)
        elif request.method == 'POST':
            response = requests.post(url, data=request.data, headers=dict(request.headers))

        response.raise_for_status()
        content_type = response.headers.get('Content-Type')

        if 'application/json' in content_type:
            return jsonify(response.json()), response.status_code
        elif 'text/html' in content_type:
            return response.text, response.status_code
        return response.text, response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run()
