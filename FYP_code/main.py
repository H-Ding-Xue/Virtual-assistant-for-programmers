from flask import Flask,redirect,url_for,render_template, request, flash
import pickle
import speech_recognition as sr
import webbrowser

app = Flask(__name__)
app.secret_key = "fyp"  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comment generation")
def comment():
    return render_template("comments.html")

@app.route("/code generation", methods=["POST","GET"])
def code():
    #get voice input
    if request.method == "POST" and request.form['btn'] == 'get_voice':
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            transcribed_text = recognizer.recognize_google(audio)
            return render_template("codes.html", transcribed_text=transcribed_text)
        except Exception as e:
            flash("Unable to process voice input - No microphone or voice detected")
            return redirect('/code generation')
    #generate code block        
    elif request.method == "POST" and request.form['btn'] == 'Generate' and request.form["pseudoinput"].strip() != '':
        loaded_vectorizer = pickle.load(open('saved_codegen_vectorizer', 'rb'))
        loaded_model = pickle.load(open('saved_codegen_model', 'rb'))
        codedesc = request.form["pseudoinput"]
        predicted_codeblock = loaded_model.predict(loaded_vectorizer.transform([codedesc]))
        predicted_codeblock = predicted_codeblock[0]
        predicted_codeblock = predicted_codeblock.replace(r'\n', '\n')
        return render_template("codes.html",predicted_codeblock=predicted_codeblock)
    elif request.method == "POST" and request.form['btn'] == 'Generate' and request.form["pseudoinput"].strip() == '': 
        flash("Pseudocode Input cannot be empty")
        return redirect('/code generation')   
    else:
        return render_template("codes.html")

@app.route("/code generation(EIEO)")
def codeEIEO():
    return render_template("codesEO.html")

@app.route("/voicebot", methods=["POST","GET"])
def voicebot():
    transcribed_text = ""
    command = False
    #get voice input
    if request.method == "POST":
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            transcribed_text = recognizer.recognize_google(audio)

            if ("google" in transcribed_text.lower()):
                command = True
                place = "Google"
                webbrowser.get('windows-default').open('https://google.com')
                return render_template("voicebot.html", transcribed_text=transcribed_text, 
                                                        command = command,
                                                        place = place)
            elif (("youtube" in transcribed_text.lower()) or 
                 ("you" in transcribed_text.lower() and "tube" in transcribed_text.lower())):
                command = True
                place = "YouTube"
                webbrowser.get('windows-default').open('https://youtube.com')
                return render_template("voicebot.html", transcribed_text=transcribed_text, 
                                                        command = command,
                                                        place = place)                               
            elif (transcribed_text != ""):
                link = "https://www.google.com/search?q=" + transcribed_text
                command = True
                webbrowser.get('windows-default').open(link)
                return render_template("voicebot.html", transcribed_text=transcribed_text, 
                                                        command = command,
                                                        place="Google search")
            else:
                flash("Unable to process command")
                return redirect('/voicebot')
        except Exception as e:
            flash("No voice or microphone detected")
            return redirect('/voicebot')
    else:
        return render_template("voicebot.html", command=command)

@app.route("/invalid_input")
def invalid_input():
    return render_template("invalid_input.html")
    
if __name__ == "__main__":
    app.run(debug = True)
