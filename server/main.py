from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes with proper headers
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/main", methods=['GET'])
def users():
    return jsonify({"user": ['totopadel']})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
