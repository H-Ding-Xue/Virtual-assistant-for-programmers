from flask import Flask,redirect,render_template, request, flash
import pickle
import speech_recognition as sr
import random
import string
from comment import comment_execution
from codetxt import code_execution
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
    if request.method == "POST" and request.form["btn"] == "Generate" and request.form["EIinput"].strip() != '' and request.form["EOinput"].strip() != '':
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
        # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        EIinput = request.values.get("EIinput")
        EOinput = request.values.get("EOinput")
        output = request.values.get("hidden")
        if output == '':
            return v.voice_assitant("codesEO.html", "/code generation(EIEO)") 
        else:
            statement = render_template("codesEO.html",inputList=EIinput,output=EOinput, predicted_output = output)
            return v.voice_assitant_with_output("codesEO.html", output, statement) 
    elif request.method == "POST" and request.form["btn"] == "Generate" and (request.form["EIinput"].strip() == '' or request.form["EOinput"].strip() == ''):
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
    if request.method == "POST" and request.form['btn'] =='Generate' and request.form["minlength"].strip() != '' and request.form["maxlength"].strip() != '' \
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
    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        output = request.values.get("hidden")
        if output == '':
            return v.voice_assitant("invalid_input.html", "/invalid_input") 
        else:
            minlength=request.values.get("minlength")
            maxlength=request.values.get("maxlength")
            charincluded=request.values.get("charincluded")
            charexcluded=request.values.get("charexcluded")
            statement = render_template("invalid_input.html", minlength=minlength,maxlength=maxlength,
                                        charincluded=charincluded,charexcluded=charexcluded,
                                        generated_output=output)
            return v.voice_assitant_with_output("invalid_input.html", output, statement)                              
    elif request.method == "POST" and request.form['btn'] =='Generate' and (request.form["minlength"].strip() == '' or request.form["maxlength"].strip() == ''):
        flash("Characters Minimum/Maximum Length cannot be empty")
        return redirect('/invalid_input')
    elif request.method == "POST" and request.form['btn'] =='Generate' and request.form["charincluded"].strip() == '' and request.form["charexcluded"].strip() == '':
        flash("You must fill up at least 'Characters must be Included' or 'Characters must be Excluded'")
        return redirect('/invalid_input')
    else:
        return render_template("invalid_input.html")
    
if __name__ == "__main__":
    app.run(debug = True)
