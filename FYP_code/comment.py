from flask import Flask,redirect,render_template, request, flash
import pickle
def comment_execution():
    code_to_english = {
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
    }
    if request.method=='POST' and request.form['generatecommentbutton'] == 'Generate' and request.form["codeinput"].strip() != '':
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
        return render_template("comments.html", codeblock=codeblock, finalstring=finalstring) 
    elif request.method=='POST' and request.form['generatecommentbutton'] == 'Generate' and request.form["codeinput"].strip() == '': 
        flash("Code Input cannot be empty")
        return redirect('/comment generation')
    else:
        return render_template("comments.html")