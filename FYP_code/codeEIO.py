from flask import redirect,render_template, request, flash
import pickle
import voicebot as v

def codeEIO_execution():
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