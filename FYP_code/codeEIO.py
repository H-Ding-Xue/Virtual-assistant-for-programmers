from flask import redirect,render_template, request, flash
import pickle
import voicebot as v

def codeEIO_execution():
    mathDict = {
        "+": "Addition",
        "-": "Subtraction",
        "*": "Multiplication",
        "/": "Division"
    }

    if request.method == "POST" and request.form["btn"] == "Generate" and request.form["EIinput"].strip() != '' and request.form["EOinput"].strip() != '':
        try:
            # check if the expected input textbox contains only int values
            inputList = [int(i) for i in request.form["EIinput"].replace(' ', '').split(',')]
        except ValueError as e:
            flash("Expected Input only accept positive integer values; separate each value with ','")
            return redirect('/code generation(EIEO)')

        # check if value is within 1 to 1000
        for value in inputList:
            if value < 1 or value > 1000:
                flash("Expected Input only accept positive integer values between 1 to 1000")
                return redirect('/code generation(EIEO)')

        if len(inputList) == 3:
            pass
        # expected input contains only 2 values, add one 0 to the list
        elif len(inputList) == 2:
            inputList.append(0)
        # expected input contains 1 or more than 3 values
        else:
            flash("Expected Input only accept between two to three positive integer values")
            return redirect('/code generation(EIEO)')
        
        try:
            # convert expected output to float value with 2dp
            output = round(float(request.form["EOinput"]), 2)
            inputList.append(output)
        except ValueError as e:
            flash("Expected Output only accept one numeric value")
            return redirect('/code generation(EIEO)')

        # load trained ML
        model = pickle.load(open('saved_codeEIO_model', 'rb'))
        prediction = model.predict([inputList])
        # load pre-defined methods
        method = pickle.load(open('saved_codeEIO_method', 'rb'))
        
        result = method[(method[['Addition', 'Subtraction', 'Multiplication', 'Division']] == prediction[0]).all(1)]
        
        predicted_output = ""
        equation = []
        answer1 = ""
        answer2 = ""
        prediction = prediction[0]
        predictionList = prediction.tolist()
        print(prediction)

        # if one-hot-encoding contains more than one 1
        if (prediction == 1).sum() > 1:
            # add predicted symbols into equation list
            for i in range(len(predictionList)):
                if predictionList[i] == 1:
                    symbol = list(mathDict)[i]
                    equation.append(symbol)
            # add expected input value into equation list
            # insert accordingly to form a proper equation
            for i in range(len(inputList) - 1):
                equation.insert(i*2, inputList[i])
            # retrieve the answer for the equation
            for value in equation:
                answer1 += str(value)
            answer1 = eval(answer1)
            # swap the symbols to form second equation
            equation[1], equation[3] = equation[3], equation[1]
            # retrieve the answer for the second equation
            for value in equation:
                answer2 += str(value)
            answer2 = eval(answer2)

            # the answers for the two equations are the same
            # and it matches with the expected output value
            if answer1 == answer2 and answer1 == inputList[-1]:
                for i in range(len(result.index)):
                    temp = method['Result'][result.index[i]]
                    predicted_output += temp.replace(r'\n', '\n')
                    predicted_output += "\n\n"
            # only the first equation matches with the expected output
            elif answer1 == inputList[-1]:
                predicted_output += method['Result'][result.index[0]]
                predicted_output = predicted_output.replace(r'\n', '\n')
            # only the second equation matches with the expected output
            elif answer2 == inputList[-1]:
                predicted_output += method['Result'][result.index[1]]
                predicted_output = predicted_output.replace(r'\n', '\n')
            # ML cannot get accurate result
            # display first result
            else:
                temp = method['Result'][result.index[0]]
                predicted_output += temp.replace(r'\n', '\n')
                predicted_output += "\n\n"
        # if one-hot-encoding contains only one 1
        else:
            predicted_output += method['Result'][result.index[0]]
            predicted_output = predicted_output.replace(r'\n', '\n')

        return render_template("codesEO.html", inputList=request.form["EIinput"], output=request.form["EOinput"], predicted_output=predicted_output)
    # voice assistant button
    elif request.method=='POST' and request.form['btn'] =='voice_assist':
        EIinput = request.values.get("EIinput")
        EOinput = request.values.get("EOinput")
        output = request.values.get("hidden")
        if output == '':
            return v.voice_assitant("codesEO.html", "/code generation(EIEO)") 
        else:
            return v.voice_assitant_with_output("codesEO.html", EIinput, EOinput, output) 
    elif request.method == "POST" and request.form["btn"] == "Generate" and (request.form["EIinput"].strip() == '' or request.form["EOinput"].strip() == ''):
        flash("Expected Input/Output cannot be empty")
        return redirect('/code generation(EIEO)')
    else:
        return render_template("codesEO.html")