from flask import Flask,redirect,url_for,render_template, request
import pickle
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comment generation")
def comment():
    return render_template("comments.html")

@app.route("/code generation", methods=["POST","GET"])
def code():
    if request.method == "POST":
        loaded_vectorizer = pickle.load(open('saved_codegen_vectorizer', 'rb'))
        loaded_model = pickle.load(open('saved_codegen_model', 'rb'))
        codedesc = request.form["pseudoinput"]
        predicted_codeblock = loaded_model.predict(loaded_vectorizer.transform([codedesc]))
        predicted_codeblock = predicted_codeblock[0]
        predicted_codeblock = predicted_codeblock.replace(r'\n', '\n')
        return render_template("codes.html",predicted_codeblock=predicted_codeblock)
    else:
        return render_template("codes.html")

@app.route("/code generation(EIEO)")
def codeEIEO():
    return render_template("codesEO.html")

@app.route("/voicebot")
def voicebot():
    return render_template("voicebot.html")

@app.route("/invalid_input")
def invalid_input():
    return render_template("invalid_input.html")
    
if __name__ == "__main__":
    app.run(debug = True)
