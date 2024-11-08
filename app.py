from flask import Flask, redirect, url_for, request, jsonify
import socket
from waitress import serve

ip = socket.gethostbyname(socket.gethostname())

app = Flask(__name__)

@app.route('/')
def home():
    return open("./static/index.html")

incomes = [
    { 'tag': 'salary', 'amount': 5000 }
]


@app.route('/getalltags')

@app.route('/getvalue', methods=['POST'])
def get_value():
    print("Request gotten")
    tag = request.args.get('tag')
    gg = request.get_json() if request.get_json() != None else "Invalid request!"
    print(f'Oh naw: {gg}')
    return gg if gg != None else "null", 200


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

@app.errorhandler(404)
def handler(error):
    print(request.path)
    pass


if __name__ == '__main__':
    print(f'Web Server at: http://{ip}:8080')
    #app.run(debug=True)
    serve(app, host=ip, port=8080, threads=1)