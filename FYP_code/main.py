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
            transcribed_text = recognizer.recognize_google(audio, language='en-GB')

            if (("code" in transcribed_text.lower() and 
                ("text" in transcribed_text.lower() or "test" in transcribed_text.lower())) 
                and ("text" in transcribed_text.lower() or "test" in transcribed_text.lower())):
                return redirect('/code generation')
            elif ("code" in transcribed_text.lower() and "expected" in transcribed_text.lower()):
                return redirect('/code generation(EIEO)')   
            elif ("comment" in transcribed_text.lower() or "common" in transcribed_text.lower() or 
                "," in transcribed_text.lower() or "comma" in transcribed_text.lower() 
                or "coleman" in transcribed_text.lower() or "command" in transcribed_text.lower()):
                return redirect('/comment generation')   
            elif ("invalid" in transcribed_text.lower() or "in valid" in transcribed_text.lower() or
            "valid" in transcribed_text.lower() or "in valley" in transcribed_text.lower()):
                return redirect('/invalid_input')   
            elif ("home" in transcribed_text.lower()):
                return redirect('/')      
            elif ("google" in transcribed_text.lower()):
                if (transcribed_text.lower() == "google"):
                    command = True
                    place = "Google"
                    webbrowser.get('windows-default').open('https://google.com')
                    return render_template("voicebot.html", transcribed_text=transcribed_text, 
                                                            command = command,
                                                            place = place)
                elif ("search" in transcribed_text.lower() and "google for" in transcribed_text.lower()):
                    query = transcribed_text.lower()
                    query = query.replace("search", "")
                    query = query.replace("google for ", "")                                           
                link = "https://www.google.com/search?q=" + query
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
