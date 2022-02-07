from flask import redirect,render_template, request, flash
import random
import string
import voicebot as v

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
        invalid_output = ""
        validString = ""
        validList = []
        valid_output = ""

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
        for included in includedList:
            if included not in letters:
                flash("'Characters must be Included' can only accept ASCII characters")
                return redirect('/invalid_input')
        for excluded in excludedList:
            if excluded not in letters:
                flash("'Characters must be Excluded' can only accept ASCII characters")
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
                invalid_output += "\n" + invalid + "\n"
            else:
                invalid_output += invalid + "\n"
        
        # valid input
        validList.append("=== String that satisfy all the requirements ===")
        for i in range(minlength, maxlength+1):
            for included in includedList:
                validString += included
            while (len(validString) != i):
                randChar = random.choice(letters)
                if randChar not in excludedList:
                    validString += randChar
            tempList = list(validString)
            random.shuffle(tempList)
            validString = ''.join(tempList)
            validList.append(validString)
            validString = ""
            tempList.clear()

        for valid in validList:
            valid_output += valid + "\n"

        return render_template("invalid_input.html", minlength=request.form["minlength"],
                                maxlength=request.form["maxlength"],
                                charincluded=request.form["charincluded"],
                                charexcluded=request.form["charexcluded"], 
                                invalid_output=invalid_output,
                                valid_output = valid_output)                        
                                
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
            return v.voice_assitant_with_output("invalid_input.html", minlength, maxlength, charincluded, charexcluded, output)                              
    elif request.method == "POST" and request.form['btn'] =='Generate' and (request.form["minlength"].strip() == '' or request.form["maxlength"].strip() == ''):
        flash("Characters Minimum/Maximum Length cannot be empty")
        return redirect('/invalid_input')
    elif request.method == "POST" and request.form['btn'] =='Generate' and request.form["charincluded"].strip() == '' and request.form["charexcluded"].strip() == '':
        flash("You must fill up at least 'Characters must be Included' or 'Characters must be Excluded'")
        return redirect('/invalid_input')
    else:
        return render_template("invalid_input.html")
