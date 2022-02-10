from flask import redirect,render_template, request, flash
import random
import string
import re
import voicebot as v

def invalid_input():
    if request.method == "POST" and request.form['btn'] =='Generate' and request.form["minlength"].strip() != '' and request.form["maxlength"].strip() != '' \
        and (request.form["charincluded"].strip() != '' or request.form["charexcluded"].strip() != ''):
        minlength = int(request.form["minlength"])
        maxlength = int(request.form["maxlength"])
        includedList = [str(i) for i in re.sub(' +', ' ', request.form["charincluded"].strip()).split(' ')]
        excludedList = [str(i) for i in re.sub(' +', ' ', request.form["charexcluded"].strip()).split(' ')]
        
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        invalidString = ""
        invalidList = []
        invalid_output = ""
        validString = ""
        validList = []
        valid_output = ""

        lowerIncludeCount = 0
        upperIncludeCount = 0
        digitsIncludeCount = 0
        punctIncludeCount = 0
        totalIncludeCount = 0
        lowerExcludeCount = 0
        upperExcludeCount = 0
        digitsExcludeCount = 0
        punctExcludeCount = 0
        totalExcludeCount = 0

        includedList.sort()
        excludedList.sort()
        
        if minlength < 1:
            flash("Character(s) Minimum Length cannot be smaller than 1")
            return redirect('/invalid_input')
        if maxlength < minlength:
            flash("'Character(s) Maximum Length' cannot be smaller than 'Character(s) Minimum Length'")
            return redirect('/invalid_input')
        if includedList[0]:
            for included in includedList:
                if len(included) != 1:
                    flash("'Character(s) must be Included' only accept single character; separate each character with a space ' '")
                    return redirect('/invalid_input')
        if excludedList[0]:
            for excluded in excludedList:
                if len(excluded) != 1:
                    flash("'Character(s) must be Excluded' only accept single character; separate each character with a space ' '")
                    return redirect('/invalid_input')
        if minlength < len(includedList):
            flash("'Character(s) Minimum Length' cannot be less than 'Character(s) must be Included'")
            return redirect('/invalid_input')
        for included in includedList:
            if included in excludedList:
                flash("'Character(s) must be Included' cannot contain characters in 'Character(s) must be Excluded'")
                return redirect('/invalid_input')
        for included in includedList:
            if included not in letters:
                flash("'Character(s) must be Included' can only accept ASCII characters")
                return redirect('/invalid_input')
        for excluded in excludedList:
            if excluded not in letters:
                flash("'Character(s) must be Excluded' can only accept ASCII characters")
                return redirect('/invalid_input')
        
        fIncludedList = list(set(includedList))
        for included in fIncludedList:
            if included in string.ascii_uppercase and included != '':
                upperIncludeCount += 1
                totalIncludeCount += 1
            elif included in string.ascii_lowercase and included != '':
                lowerIncludeCount += 1
                totalIncludeCount += 1
            elif included in string.digits and included != '':
                digitsIncludeCount += 1
                totalIncludeCount += 1
            elif included in string.punctuation and included != '':
                punctIncludeCount += 1
                totalIncludeCount += 1

        fExcludedList = list(set(excludedList))
        for excluded in fExcludedList:
            if excluded in string.ascii_uppercase and excluded != '':
                upperExcludeCount += 1
                totalExcludeCount += 1
            elif excluded in string.ascii_lowercase and excluded != '':
                lowerExcludeCount += 1
                totalExcludeCount += 1
            elif excluded in string.digits and excluded != '':
                digitsExcludeCount += 1
                totalExcludeCount += 1
            elif excluded in string.punctuation and excluded != '':
                punctExcludeCount += 1
                totalExcludeCount += 1
            if totalExcludeCount == len(letters):
                flash("'Character(s) must be Excluded' cannot contain all ASCII characters")
                return redirect('/invalid_input')

        if upperIncludeCount == len(string.ascii_uppercase):
            uppercaseI = "checked"
        else:
            uppercaseI = ""
        if lowerIncludeCount == len(string.ascii_lowercase):
            lowercaseI = "checked"
        else:
            lowercaseI = ""
        if punctIncludeCount == len(string.punctuation):
            symbolsI = "checked"
        else:
            symbolsI = ""
        if digitsIncludeCount == len(string.digits):
            numbersI = "checked"
        else:
            numbersI = ""
        
        if upperExcludeCount == len(string.ascii_uppercase):
            uppercaseE = "checked"
        else:
            uppercaseE = ""
        if lowerExcludeCount == len(string.ascii_lowercase):
            lowercaseE = "checked"
        else:
            lowercaseE = ""
        if punctExcludeCount == len(string.punctuation):
            symbolsE = "checked"
        else:
            symbolsE = ""
        if digitsExcludeCount == len(string.digits):
            numbersE = "checked"
        else:
            numbersE = ""

        # valid string but doesn't meet the minimum length requirement
        if minlength != 1:
            invalidList.append("=== Input that doesn't meet the minimum length requirement ===")
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
        invalidList.append("=== Input that doesn't meet the maximum length requirement ===")
        for included in includedList:
            invalidString += included
        while (len(invalidString) != maxlength+1):
            randChar = random.choice(letters)
            if randChar not in excludedList:
                invalidString += randChar
        invalidList.append(invalidString)
        invalidString = ""
        
        # invalid string (doesn't contain all the characters in 'Characters must be Included')
        if includedList[0]:
            invalidList.append("=== Input that doesn't contain all the characters in 'Character(s) must be Included' ===")
            if totalIncludeCount + totalExcludeCount == len(letters):
                for included in includedList:
                    if len(includedList) != 1:
                        invalidString = included
                    else:
                        invalidString = ""
                    charCount = random.randint(minlength, maxlength)
                    while (len(invalidString) != charCount):
                        randChar = random.choice(letters)
                        if randChar != fIncludedList[-1]:
                            if randChar not in excludedList:
                                invalidString += randChar
                    invalidList.append(invalidString)
                    invalidString = ""
            else:
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
            invalidList.append("=== Input that contains characters in 'Characters must be Excluded' ===")
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
        validList.append("=== Input that satisfy all the requirements ===")
        for i in range(minlength, maxlength+1):
            for included in includedList:
                validString += included
            while (len(validString) != i):
                randChar = random.choice(letters)
                if randChar not in excludedList:
                    validString += randChar
            temp = list(validString)
            random.shuffle(temp)
            validString = ''.join(temp)
            validList.append(validString)
            validString = ""

        for valid in validList:
            valid_output += valid + "\n"

        return render_template("invalid_input.html", minlength=request.form["minlength"],
                                maxlength=request.form["maxlength"],
                                charincluded=request.form["charincluded"],
                                charexcluded=request.form["charexcluded"], 
                                uppercaseI=uppercaseI,
                                lowercaseI=lowercaseI,
                                symbolsI=symbolsI,
                                numbersI=numbersI,
                                uppercaseE=uppercaseE,
                                lowercaseE=lowercaseE,
                                symbolsE=symbolsE,
                                numbersE=numbersE,
                                invalid_output=invalid_output,
                                valid_output = valid_output)                        
                                
    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        invalid_output = request.values.get("hidden_iv")
        if invalid_output == '':
            return v.voice_assitant("invalid_input.html", "/invalid_input") 
        else:
            valid_output = request.values.get("hidden_v")
            minlength=request.values.get("minlength")
            maxlength=request.values.get("maxlength")
            charincluded=request.values.get("charincluded")
            charexcluded=request.values.get("charexcluded")
            return v.voice_assitant_with_output("invalid_input.html", minlength, maxlength, charincluded, charexcluded, invalid_output, valid_output)                              
    elif request.method == "POST" and request.form['btn'] =='Generate' and (request.form["minlength"].strip() == '' or request.form["maxlength"].strip() == ''):
        flash("Characters Minimum/Maximum Length cannot be empty")
        return redirect('/invalid_input')
    elif request.method == "POST" and request.form['btn'] =='Generate' and request.form["charincluded"].strip() == '' and request.form["charexcluded"].strip() == '':
        flash("You must fill up at least 'Characters must be Included' or 'Characters must be Excluded'")
        return redirect('/invalid_input')
    else:
        return render_template("invalid_input.html")
