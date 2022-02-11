from flask import Flask,redirect,render_template, request, flash
import pickle
import voicebot as v

def comment_execution():
    code_to_english = {
        '++': " increment ",
        '--': " decrement ",
        '"r+"': " read and write ",
        "'r+'": " read and write ",
        "+=": " assign add ",
        "/=": " assign divide ",
        "*=": " assign multiply ",
        "-=": " assign minus ",
        "==": " same ",
        "!=": " not same ",
        "<=": " smaller or equal ",
        ">=": " bigger or equal ",
        "<": " lesser ",
        ">": " greater ",
        "elif": " else if ",
        "=": " assign ",
        "+": " add ",
        "-": " minus ",
        "*": " multiply ",
        "/": " divide ",
        "range": " range ",
        "while": " while ",
        "if": " if ",
        "else": " else ",
        "print": " print ",
        "try": " try ",
        "except": " except ",
        "NameError": " name error ",
        "TypeError": " type error ",
        "ValueError": " value error ",
        "KeyError": " lookup error ",
        "IndexError": " lookup error ",
        "input": " input ",
        "def": " method ",
        "__init__": " construct ",
        'open': " open ",
        'close': " close ",
        "readlines": " read lines ",
        "readline": " read line ",
        "read": " read ",
        "self": " self ",
        '"a"': " append ",
        '"r"': " read ",
        '"w"': " write ",
        "'r'": " read ",
        "'w'": " write ",
        "'a'": " append ",
        ".": " dot ",
        "write": " write "
    }
    if request.method=='POST' and request.form['btn'] == 'Generate' and request.form["codeinput"].strip() != '' and request.form["Mode"]=='lbl':
        Selected='lbl'
        codeblock = request.form["codeinput"]
        linebyline = codeblock.split('\n')
        commentlist = []
        loaded_vectorizer = pickle.load(open('saved_comgen_vectorizer', 'rb'))
        loaded_model = pickle.load(open('saved_comgen_model', 'rb'))
        for i in range(len(linebyline)):
            linebyline[i] = linebyline[i].replace('\r','')

        for i in range(len(linebyline)):
            Comment = linebyline[i]
            if Comment.isspace() or Comment=='\r'or Comment=='\n'or Comment=='':
                commentlist.append("")
            else:
                for key, value in code_to_english.items():
                    if key in Comment:
                        Comment = Comment.replace(key,value)
                commentlist.append(loaded_model.predict(loaded_vectorizer.transform([Comment]))[0])
        finalstring = ''
        for i in range(len(linebyline)):
            if not linebyline[i].isspace() and linebyline[i]!='' and linebyline[i]!='\r' and linebyline[i]!='\n':
                finalstring = finalstring + linebyline[i] +' # '+ commentlist[i] + '\n'
            else:
                finalstring = finalstring + linebyline[i] + commentlist[i] + '\n'
        return render_template("comments.html", codeblock=codeblock, finalstring=finalstring, Selected=Selected) 
    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        codeblock = request.values.get("codeinput")
        finalstring = request.values.get("hidden")
        if finalstring == '':
            return v.voice_assitant("comments.html", "/comment generation") 
        else:
            return v.voice_assitant_with_output("comments.html", codeblock, finalstring)         
    elif request.method=='POST' and request.form['btn'] == 'Generate' and request.form["codeinput"].strip() == '': 
        flash("Code Input cannot be empty")
        return redirect('/comment generation')
    elif request.method=='POST' and request.form['btn'] == 'Generate' and request.form["codeinput"].strip() != '' and request.form["Mode"]=='all':
        Selected='all'
        codeblock = request.form["codeinput"]
        codeblock2 = codeblock
        for key, value in code_to_english.items():
                    if key in codeblock2:
                        codeblock2 = codeblock2.replace(key,value)
        loaded_vectorizer = pickle.load(open('saved_comgen_vectorizer2', 'rb'))
        loaded_model = pickle.load(open('saved_comgen_model2', 'rb'))
        finalstring = loaded_model.predict(loaded_vectorizer.transform([codeblock2]))[0]
        
        
        return render_template("comments.html", codeblock=codeblock, finalstring=finalstring,Selected=Selected)
    else:
        return render_template("comments.html")