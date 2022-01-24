from flask import Flask,redirect,render_template, request, flash
import pickle
import speech_recognition as sr
import random
import string

import voicebot as v

app = Flask(__name__)
app.secret_key = "fyp"  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/comment generation", methods=["POST","GET"])
def comment():
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

@app.route("/code generation", methods=["POST","GET"])
def code():
    #get voice input
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

@app.route("/code generation(EIEO)", methods=["POST","GET"])
def codeEIEO():
    if request.method == "POST" and request.form["EIinput"].strip() != '' and request.form["EOinput"].strip() != '':
        try:
            inputList = [int(i) for i in request.form["EIinput"].replace(' ', '').split(',')]
        except ValueError as e:
            flash("Expected Input only accept integer values; separate each value with ','")
            return redirect('/code generation(EIEO)')

        if len(inputList) == 3:
            pass
        elif len(inputList) == 2:
            inputList.append(0)
        elif len(inputList) == 1:
            inputList.append(0)
            inputList.append(0)
        else:
            flash("Expected Input only accept up to three integer values; separate each value with ','")
            return redirect('/code generation(EIEO)')
        
        try:
            output = round(float(request.form["EOinput"]), 2)
            inputList.append(output)
        except ValueError as e:
            flash("Expected Output only accept one numeric value")
            return redirect('/code generation(EIEO)')

        model = pickle.load(open('saved_codeEO_model', 'rb'))
        print(inputList)
        prediction = model.predict([inputList])
        print(prediction)
        with open('saved_codeEO_method', 'rb') as f:
            df = pickle.load(f)
        
        result = df[(df[['Addition', 'Division', 'Multiplication', 'Subtraction', 'Equals']] == prediction[0]).all(1)]
        print(result)
        predicted_output = ""
        for i in range(len(result.index)):
            temp = df['Result'][result.index[i]]
            predicted_output += temp.replace(r'\n', '\n')
            predicted_output += "\n\n"

        return render_template("codesEO.html", inputList=request.form["EIinput"], output=request.form["EOinput"], predicted_output=predicted_output)
    elif request.method == "POST" and (request.form["EIinput"].strip() == '' or request.form["EOinput"].strip() == ''):
        flash("Expected Input/Output cannot be empty")
        return redirect('/code generation(EIEO)')
    else:
        return render_template("codesEO.html")

@app.route("/voicebot", methods=["POST","GET"])
def voicebot():
    if request.method == "POST":
        return v.voice_assitant("voicebot.html", "/voicebot")
    else:
        return render_template("voicebot.html")

@app.route("/invalid_input", methods=["POST","GET"])
def invalid_input():
    if request.method == "POST" and request.form["minlength"].strip() != '' and request.form["maxlength"].strip() != '' \
        and (request.form["charincluded"].strip() != '' or request.form["charexcluded"].strip() != ''):
        minlength = int(request.form["minlength"])
        maxlength = int(request.form["maxlength"])
        includedList = [str(i) for i in request.form["charincluded"].replace('  ', ' ').split(' ')]
        excludedList = [str(i) for i in request.form["charexcluded"].replace('  ', ' ').split(' ')]
        
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        invalidString = ""
        invalidList = []
        generated_output = ""

        includedList.sort()
        excludedList.sort()
        
        if minlength < 1:
            flash("Characters Minimum Length cannot be smaller than 1")
            return redirect('/invalid_input')
        if maxlength < minlength:
            flash("'Characters Maximum Length' cannot be smaller than 'Characters Minimum Length'")
            return redirect('/invalid_input')
        if includedList[0]:
            for included in includedList:
                if len(included) != 1:
                    flash("'Characters must be Included' only accept single character; separate each character with space ' '")
                    return redirect('/invalid_input')
        if excludedList[0]:
            for excluded in excludedList:
                if len(excluded) != 1:
                    flash("'Characters must be Excluded' only accept single character; separate each character with space ' '")
                    return redirect('/invalid_input')
        if minlength < len(includedList):
            flash("'Characters Minimum Length' cannot be less than 'Characters must be Included'")
            return redirect('/invalid_input')
        for included in includedList:
            if included in excludedList:
                flash("'Characters must be Included' cannot contain characters in 'Characters must be Excluded'")
                return redirect('/invalid_input')
        
        
        # valid string but doesn't meet the minimum length requirement
        if minlength != 1:
            invalidList.append("=== String that doesn't meet the minimum length requirement ===")
            for included in includedList:
                invalidString += included
            if len(includedList) == minlength:
                invalidString = invalidString[:-1]
            while (len(invalidString) != minlength-1):
                randChar = random.choice(letters)
                if randChar not in excludedList:
                    invalidString += randChar
            invalidList.append(invalidString)
            invalidString = ""
        
        # valid string but doesn't meet the maximum length requirement
        invalidList.append("=== String that doesn't meet the maximum length requirement ===")
        for included in includedList:
            invalidString += included
        while (len(invalidString) != maxlength+1):
            randChar = random.choice(letters)
            if randChar not in excludedList:
                invalidString += randChar
        invalidList.append(invalidString)
        invalidString = ""
        
        # invalid string (doesn't contain all the characters in 'Characters must be included')
        if includedList[0]:
            invalidList.append("=== String that doesn't contain all the characters in 'Characters must be Included' ===")
            for included in includedList:
                if len(includedList) != 1:
                    invalidString = included
                else:
                    invalidString = ""
                charCount = random.randint(minlength, maxlength)
                while (len(invalidString) != charCount):
                    randChar = random.choice(letters)
                    if randChar not in includedList:
                        if randChar not in excludedList:
                            invalidString += randChar
                invalidList.append(invalidString)
                invalidString = ""
        
        # invalid string (contains characters in 'Characters must be excluded')
        if excludedList[0]:
            invalidList.append("=== String that contains characters in 'Characters must be Excluded' ===")
            for excluded in excludedList:
                for included in includedList:
                    invalidString += included
                while len(invalidString) == maxlength:
                    invalidString = invalidString[:-1]
                invalidString += excluded
                charCount = random.randint(minlength, maxlength)
                if len(invalidString) < charCount:
                    while(len(invalidString) != charCount):
                        randChar = random.choice(letters)
                        invalidString += randChar
                invalidList.append(invalidString)
                invalidString = ""

        for invalid in invalidList:
            if " ===" in invalid:
                generated_output += "\n" + invalid + "\n"
            else:
                generated_output += invalid + "\n"

        return render_template("invalid_input.html", minlength=request.form["minlength"],
                                maxlength=request.form["maxlength"],
                                charincluded=request.form["charincluded"],
                                charexcluded=request.form["charexcluded"], 
                                generated_output=generated_output)
    elif request.method == "POST" and (request.form["minlength"].strip() == '' or request.form["maxlength"].strip() == ''):
        flash("Characters Minimum/Maximum Length cannot be empty")
        return redirect('/invalid_input')
    elif request.method == "POST" and request.form["charincluded"].strip() == '' and request.form["charexcluded"].strip() == '':
        flash("You must fill up at least 'Characters must be Included' or 'Characters must be Excluded'")
        return redirect('/invalid_input')
    else:
        return render_template("invalid_input.html")
    
if __name__ == "__main__":
    app.run(debug = True)
