from flask import Flask,redirect,render_template, request, flash
import pickle
import voicebot as v
def code_execution():
    #get text from voice input
    if request.method == "POST" and request.form['btn'] == 'get_voice':
        try:
            text = v.convert_word()
            return render_template("codes.html", transcribed_text=text)
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
        return render_template("codes.html",codedesc=codedesc,predicted_codeblock=predicted_codeblock)
    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        input = request.values.get("pseudoinput")
        output = request.values.get("hidden")
        if output == '':
            return v.voice_assitant("codes.html", "/code generation") 
        else:
            statement = render_template("codes.html",codedesc=input,predicted_codeblock=output)
            return v.voice_assitant_with_output("codes.html", output, statement)           
    elif request.method == "POST" and request.form['btn'] == 'Generate' and request.form["pseudoinput"].strip() == '': 
        flash("Pseudocode Input cannot be empty")
        return redirect('/code generation')   
    else:
        return render_template("codes.html")