from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

@app.route('/', methods=['GET'])
def proxy_api_data():
    api_endpoint = 'http://44.214.182.154:4000/'
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run()
