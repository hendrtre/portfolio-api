from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Trent!"

if __name__ == "__main__":
    app.debug = True
    app.run()