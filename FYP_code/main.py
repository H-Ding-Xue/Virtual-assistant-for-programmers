from flask import Flask,redirect,render_template, request, flash
import random
import string
from comment import comment_execution
from codetxt import code_execution
from codeEIO import codeEIO_execution
from invalidInput import invalid_input
import voicebot as v

app = Flask(__name__)
app.secret_key = "fyp"  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comment generation", methods=["POST","GET"])
def comment():
    return comment_execution()

@app.route("/code generation", methods=["POST","GET"])
def code():
    return code_execution()
   

@app.route("/code generation(EIEO)", methods=["POST","GET"])
def codeEIEO():
    return codeEIO_execution()

@app.route("/voicebot", methods=["POST","GET"])
def voicebot():
    if request.method == "POST":
        return v.voice_assitant("voicebot.html", "/voicebot")
    else:
        return render_template("voicebot.html")

@app.route("/invalid_input", methods=["POST","GET"])
def invalidInput():
    return invalid_input()

if __name__ == "__main__":
    app.run(debug = True)
