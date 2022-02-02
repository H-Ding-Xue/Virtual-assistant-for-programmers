from flask import Flask,redirect,render_template, request, flash
import pickle
import voicebot as v 
def code_execution():
    #generate code block        
    if request.method == "POST" and request.form['btn'] == 'Generate' and request.form["pseudoinput"].strip() != '':
        pseudoblock = request.form["pseudoinput"]
        linebyline = pseudoblock.split('\n')
        codelist = []
        loaded_vectorizer = pickle.load(open('saved_codegen_vectorizer', 'rb'))
        loaded_model = pickle.load(open('saved_codegen_model', 'rb'))
        for i in range(len(linebyline)):
            linebyline[i] = linebyline[i].replace('\r','')
            

        for i in range(len(linebyline)):
            pseudocode = linebyline[i]
            if pseudocode.isspace() or pseudocode=='\r'or pseudocode=='\n'or pseudocode=='':
                codelist.append("")
            else:
                codelist.append(loaded_model.predict(loaded_vectorizer.transform([pseudocode]))[0])
        predicted_codeblock = ''
        for i in range(len(linebyline)):
            if not linebyline[i].isspace() and linebyline[i]!='' and linebyline[i]!='\r' and linebyline[i]!='\n':
                leadingSpaces=''
                for element in linebyline[i]:
                    if not element.isspace():
                        break
                    leadingSpaces = leadingSpaces + element
                codelist[i] = codelist[i].replace(r'\n', '\n')
                predicted_codeblock = predicted_codeblock +leadingSpaces+  codelist[i] + '\n'
            else:
                predicted_codeblock = predicted_codeblock + '\n'
        return render_template("codes.html", pseudoblock=pseudoblock, predicted_codeblock=predicted_codeblock)

    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        input = request.values.get("pseudoinput")
        output = request.values.get("hidden")
        if output == '':
            return v.voice_assitant("codes.html", "/code generation") 
        else:
            return v.voice_assitant_with_output("codes.html", input, output)           
    elif request.method == "POST" and request.form['btn'] == 'Generate' and request.form["pseudoinput"].strip() == '': 
        flash("Pseudocode Input cannot be empty")
        return redirect('/code generation')   
    else:
        return render_template("codes.html")