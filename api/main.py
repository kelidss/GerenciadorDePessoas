from flask import Flask, request, jsonify

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/hello", methods=["GET"])
    def hello():
        return "ola"

    app.run(host="0.0.0.0", port=5000)