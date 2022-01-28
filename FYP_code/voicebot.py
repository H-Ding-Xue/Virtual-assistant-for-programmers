from flask import redirect,render_template, flash, request
import speech_recognition as sr
import webbrowser
import datetime
import subprocess

# similar sounding words with target words
similar_sounding_words = {
    "no pet": "notepad",
    "not pet": "notepad",
    "noah pet": "notepad",
    "note pad": "notepad",
    "sing": "syntax",
    "singtel": "syntax",
    "sing tips": "syntax",
    "sing text" : "syntax",
    "common": "comment",
    "comma": "comment",
    "command": "comment",
    "commence" : "comment",
    "coleman" : "comment",
    "bearable": "variable",
    "favorable" : "variable", 
    "Bela Bose" : "variable",
    "numbness" : "numbers",
    "testing" : "casting",
    "Beast" : "list",
    "this" : "list",
    "topo" : "tuple",
    "tapas" : "tuple",
    "topple" : "tuple",
    "apple" : "tuple",
    "wow" : "while",
    "follow" : "for loop",
    "funshion" : "function",
    "a ray" : "array",
    "w3school" : "w3schools",
    "date time": "datetime"
}

#keywords and corresponding w3school links
w3_links ={
    "syntax" : "https://www.w3schools.com/python/python_syntax.asp",
    "comments": "https://www.w3schools.com/python/python_comments.asp",
    "comment": "https://www.w3schools.com/python/python_comments.asp",
    "variable": "https://www.w3schools.com/python/python_variables.asp",
    "variables": "https://www.w3schools.com/python/python_variables.asp",
    "data type": "https://www.w3schools.com/python/python_datatypes.asp",
    "data types": "https://www.w3schools.com/python/python_datatypes.asp",
    "number": "https://www.w3schools.com/python/python_numbers.asp",
    "numbers": "https://www.w3schools.com/python/python_numbers.asp",
    "cast": "https://www.w3schools.com/python/python_casting.asp",
    "casting": "https://www.w3schools.com/python/python_casting.asp",
    "string": "https://www.w3schools.com/python/python_strings.asp",
    "strings": "https://www.w3schools.com/python/python_strings.asp",
    "boolean" : "https://www.w3schools.com/python/python_booleans.asp",
    "booleans" : "https://www.w3schools.com/python/python_booleans.asp",
    "operator" : "https://www.w3schools.com/python/python_operators.asp",
    "operators" : "https://www.w3schools.com/python/python_operators.asp",
    "list" : "https://www.w3schools.com/python/python_lists.asp",
    "lists" : "https://www.w3schools.com/python/python_lists.asp",
    "tuple" : "https://www.w3schools.com/python/python_tuples.asp",
    "tuples" : "https://www.w3schools.com/python/python_tuples.asp",
    "set" : "https://www.w3schools.com/python/python_sets.asp",
    "sets" : "https://www.w3schools.com/python/python_sets.asp",
    "dictonary" : "https://www.w3schools.com/python/python_dictionaries.asp",
    "dictonaries" : "https://www.w3schools.com/python/python_dictionaries.asp",
    "if else" : "https://www.w3schools.com/python/python_conditions.asp",
    "while" : "https://www.w3schools.com/python/python_while_loops.asp",
    "for loop" : "https://www.w3schools.com/python/python_for_loops.asp",
    "for loops" : "https://www.w3schools.com/python/python_for_loops.asp",
    "function" : "https://www.w3schools.com/python/python_functions.asp",
    "functions" : "https://www.w3schools.com/python/python_functions.asp",
    "lambda" : "https://www.w3schools.com/python/python_lambda.asp",
    "array" : "https://www.w3schools.com/python/python_arrays.asp",
    "arrays" : "https://www.w3schools.com/python/python_arrays.asp",
    "classes" : "https://www.w3schools.com/python/python_classes.asp",
    "objects" : "https://www.w3schools.com/python/python_classes.asp",
    "class" : "https://www.w3schools.com/python/python_classes.asp",
    "object" : "https://www.w3schools.com/python/python_classes.asp",
    "inheritance" : "https://www.w3schools.com/python/python_inheritance.asp",
    "date" : "https://www.w3schools.com/python/python_datetime.asp",
    "datetime" : "https://www.w3schools.com/python/python_datetime.asp",
    "dates" : "https://www.w3schools.com/python/python_datetime.asp",
    "math" : "https://www.w3schools.com/python/python_math.asp",
    "maths" : "https://www.w3schools.com/python/python_math.asp",
    "try except" : "https://www.w3schools.com/python/python_try_except.asp",
    "try" : "https://www.w3schools.com/python/python_try_except.asp",
    "except" : "https://www.w3schools.com/python/python_try_except.asp",
    "user" : "https://www.w3schools.com/python/python_user_input.asp",
    "user input" : "https://www.w3schools.com/python/python_user_input.asp",
    "format" : "https://www.w3schools.com/python/python_string_formatting.asp",
    "file": "https://www.w3schools.com/python/python_file_handling.asp",
    "read": "https://www.w3schools.com/python/python_file_open.asp",
    "write": "https://www.w3schools.com/python/python_file_write.asp"
}

# get voice and convert to text
def get_text_from_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source, timeout=5)
    transcribed_text = recognizer.recognize_google(audio, language='en-GB')
    return transcribed_text

# redirect to pages within the app
def redirect_to_app_page(transcribed_text):
    within_page= True
    page = ""
    if not("w3schools" in transcribed_text.lower() or "w3school" in transcribed_text.lower()):
        #redirecting to various pages if keyword found in transcribed text
        if (("code" in transcribed_text.lower() and 
            ("text" in transcribed_text.lower() or "test" in transcribed_text.lower())) 
            and ("text" in transcribed_text.lower() or "test" in transcribed_text.lower())):
            page ='/code generation'
        elif ("code" in transcribed_text.lower() and "expected" in transcribed_text.lower()):
            return '/code generation(EIEO)'   
        elif ("comment" in transcribed_text.lower() or "common" in transcribed_text.lower() or 
            "," in transcribed_text.lower() or "comma" in transcribed_text.lower() 
            or "coleman" in transcribed_text.lower() or "command" in transcribed_text.lower()):
            page ='/comment generation'   
        elif ("invalid" in transcribed_text.lower() or "in valid" in transcribed_text.lower() or
        "valid" in transcribed_text.lower() or "in valley" in transcribed_text.lower()):
            page = '/invalid_input'   
        elif ("home" in transcribed_text.lower()):
            page = "/"
        else:
            within_page = False
    else:
        within_page = False        
    return within_page, page

#redirect to google
def redirect_to_google(transcribed_text):
    if (transcribed_text.lower() == "google"):
        command = True
        place = "Google"
        webbrowser.open("https://www.google.com/")
    #if keywords contain google for get the keywords accordingly
    elif ("search" in transcribed_text.lower() and "google for" in transcribed_text.lower()):
        query = transcribed_text.lower()
        query = query.replace("search", "")
        query = query.replace("google for ", "")                                           
        link = "https://www.google.com/search?q=" + query
        command = True
        place="Google search"
        webbrowser.open(link)
    else:
        command = False
        place = "Google" 
    return command, place

#redirect to w3schools
def redirect_to_w3schools(transcribed_text):
    command = True
    #if keyword contains only w3schools open w3schools python page 
    if (transcribed_text.lower() == "w3schools"):
        place = "w3schools Python Tutorial"
        webbrowser.open("https://www.w3schools.com/python/default.asp")
    else:
        link = ""
        #search if text is found in the w3_links dictionary
        for key, value in w3_links.items():
            if key in transcribed_text:
                link = value
        # if found, direct to the page        
        if link != "":
            webbrowser.open(link)
            place = "w3schools"
        # if not found, redirect to google to search for the page    
        else:    
            query = transcribed_text.lower()
            query = query.replace("w3schools ", "")
            link = "https://www.google.com/search?q=" + "site:https://www.w3schools.com/python/ " + query
            webbrowser.open(link)
            place = "Google" 
    return command, place

# check if there are any similar sounding words and convert it
def convert_word():
    transcribed_text = get_text_from_speech()
    for key, value in similar_sounding_words.items():
        if key in transcribed_text.lower():
            transcribed_text = transcribed_text.replace(key,value)
    return transcribed_text    

# call the redirect_to_google and redirect_to_w3schools in one function
def redirect_to_webpages(transcribed_text):
    if ("google" in transcribed_text.lower()):
        command, place = redirect_to_google(transcribed_text) 
    elif ("w3schools" in transcribed_text.lower()):  
        command, place = redirect_to_w3schools(transcribed_text)                                     
    else:
        command = False
        place = None                                      
    return command, place

#generate file name based on current datetime
def get_filename():
    current_datetime = datetime.datetime.now()
    format_datetime = current_datetime.strftime("%d%m%y_%H%I%M%S")
    filename = "va_" + format_datetime + ".txt"
    return filename

# open notepad
def open_notepad():
    filename = get_filename()
    f = open(filename, "w")
    f.close()
    try:
        webbrowser.open(filename)
        open_empty_success = True
    except Exception:
        open_empty_success = False
    return open_empty_success    


#write output to notepad file
def copy_to_notepad(output):
    filename = get_filename()
    with open(filename, 'w') as out_file:
        out_file.write(output)
    out_file.close()
    try:
        webbrowser.open(filename)
        open_success = True
    except Exception:
        open_success = False
    return open_success


#calling this function from main if no output is available
def voice_assitant(current_page, path):
    try:
        #get voice and fix similar sounding words
        text = convert_word()
        #check if redirection is within the webapp
        within_page, page = redirect_to_app_page(text)
        #return directed page if true
        if within_page == True:
            statement = redirect(page)
        #open notepad if notepad 
        elif ("notepad" in text.lower()):
            open_empty_success = open_notepad()
            statement = render_template(current_page, open_empty_success=open_empty_success)
        else:
            #redirect to google/w3school
            command, place = redirect_to_webpages(text)
            if command == True:
                statement = render_template(current_page, transcribed_text=text, 
                                                        command = command,
                                                        place = place)
            #if keyword contains google but wrong commands
            elif command == False and page == "Google":
                flash("Start command with 'Google For' to search google with query results displayed")
                statement = redirect(path)
            else:
                flash("Unable to process command")
                statement = redirect(path)
    except Exception as e:
            flash("No voice or microphone detected")
            statement = redirect(path)
    return statement   

#calling this function from main if output is available
def voice_assitant_with_output(current_page, *args):
    try:
        #get voice and fix similar sounding words
        text = convert_word()
        #check if redirection is within the webapp
        within_page, page = redirect_to_app_page(text)
        #return directed page if true
        if within_page == True:
            statement = redirect(page)
        #write output notepad if notepad or copy word is found 
        elif ("notepad" in text.lower() or "copy" in text.lower()):
            write_success = copy_to_notepad(*args[-1])
            statement = render_page_with_output_in_editor(current_page, write_success, *args)
        else:
            #redirect to google/w3school
            command, place = redirect_to_webpages(text)
            if command == True:
                statement = render_page_with_popup(current_page, text,command,place, *args)
            #if keyword contains google but wrong commands
            elif command == False and page == "Google":
                flash("Start command with 'Google For' to search google with query results displayed")
                statement = render_correct_page(current_page, *args)
            else:
                flash("Unable to process command")
                statement = render_correct_page(current_page, *args)
    except Exception as e:
            flash("No voice or microphone detected")
            statement = render_correct_page(current_page, *args)
    return statement   


def render_page_with_output_in_editor(current_page, write_success, *args):
    if current_page == "invalid_input.html":
        return render_template(current_page, minlength=args[0],maxlength=args[1],
                         charincluded=args[2],charexcluded=args[3],
                         generated_output=args[-1], write_output=write_success)
    elif current_page == "comments.html":
        return render_template(current_page, codeblock=args[0],finalstring=args[1],
                               write_output=write_success)
    elif current_page == "codesEO.html":
        return render_template(current_page, inputList=args[0],output=args[1], predicted_output=args[2],
                               write_output=write_success)
    else:
        return render_template(current_page, codedesc=args[0],predicted_codeblock=args[1],
                               write_output=write_success)


def render_page_with_popup(current_page, transcribed_text, command, place, *args):
    if current_page == "invalid_input.html":
        return render_template(current_page, minlength=args[0],maxlength=args[1],
                         charincluded=args[2],charexcluded=args[3],
                         generated_output=args[-1], transcribed_text=transcribed_text,
                         command=command, place= place)
    elif current_page == "comments.html":
        return render_template(current_page, codeblock=args[0],finalstring=args[1],
                               transcribed_text=transcribed_text, command=command, 
                               place= place)
    elif current_page == "codesEO.html":
        return render_template(current_page, inputList=args[0],output=args[1], predicted_output=args[2],
                               transcribed_text=transcribed_text, command=command, place= place)
    else:
        return render_template(current_page, codedesc=args[0],predicted_codeblock=args[1],
                               transcribed_text=transcribed_text, command=command, 
                               place= place)

def render_correct_page(current_page, *args):
    if current_page == "invalid_input.html":
        return render_template(current_page, minlength=args[0],maxlength=args[1],
                         charincluded=args[2],charexcluded=args[3],
                         generated_output=args[-1])
    elif current_page == "comments.html":
        return render_template(current_page, codeblock=args[0],finalstring=args[1])
    elif current_page == "codesEO.html":
        return render_template(current_page, inputList=args[0],output=args[1], predicted_output=args[2])
    else:
        return render_template(current_page, codedesc=args[0],predicted_codeblock=args[1])        