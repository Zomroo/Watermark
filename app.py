from flask import Flask, request, jsonify
from filename import your_function # Replace 'your_function' with the name of the function you want to run

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to my Flask app!'})

@app.route('/run_function', methods=['POST'])
def run_function():
    data = request.get_json()
    result = your_function(data['input'])
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
