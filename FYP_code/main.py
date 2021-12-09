from flask import Flask,redirect,url_for,render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comment generation")
def comment():
    return render_template("comments.html")

@app.route("/code generation")
def code():
    return render_template("codes.html")

@app.route("/voicebot")
def voicebot():
    return render_template("voicebot.html")

@app.route("/invalid_input")
def invalid_input():
    return render_template("invalid_input.html")
    
if __name__ == "__main__":
    app.run(debug = True)
