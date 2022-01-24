from flask import redirect,render_template, flash
import speech_recognition as sr
import webbrowser
import datetime
import subprocess

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
def get_text_from_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source, timeout=5)
    transcribed_text = recognizer.recognize_google(audio, language='en-GB')
    return transcribed_text

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

def redirect_to_google(transcribed_text):
    if (transcribed_text.lower() == "google"):
        command = True
        place = "Google"
        webbrowser.get('windows-default').open("https://www.google.com/")
    elif ("search" in transcribed_text.lower() and "google for" in transcribed_text.lower()):
        query = transcribed_text.lower()
        query = query.replace("search", "")
        query = query.replace("google for ", "")                                           
        link = "https://www.google.com/search?q=" + query
        command = True
        place="Google search"
        webbrowser.get('windows-default').open(link)
    else:
        command = False
        place = "Google" 
    return command, place

def redirect_to_w3schools(transcribed_text):
    command = True
    if (transcribed_text.lower() == "w3schools"):
        place = "w3schools Python Tutorial"
        webbrowser.get('windows-default').open("https://www.w3schools.com/python/default.asp")
    else:
        link = ""
        for key, value in w3_links.items():
            if key in transcribed_text:
                link = value
        if link != "":
            webbrowser.get('windows-default').open(link)
            place = "w3schools"
        else:    
            query = transcribed_text.lower()
            query = query.replace("w3schools ", "")
            link = "https://www.google.com/search?q=" + "site:https://www.w3schools.com/python/ " + query
            webbrowser.get('windows-default').open(link)
            place = "Google" 
    return command, place

def convert_word():
    transcribed_text = get_text_from_speech()
    for key, value in similar_sounding_words.items():
        if key in transcribed_text.lower():
            transcribed_text = transcribed_text.replace(key,value)
    return transcribed_text    

def redirect_to_webpages(transcribed_text):
    if ("google" in transcribed_text.lower()):
        command, place = redirect_to_google(transcribed_text) 
    elif ("w3schools" in transcribed_text.lower()):  
        command, place = redirect_to_w3schools(transcribed_text)                                     
    else:
        command = False
        place = None                                      
    return command, place

def get_filename():
    current_datetime = datetime.datetime.now()
    format_datetime = current_datetime.strftime("%d%m%y_%H%I%M%S")
    filename = "va_" + format_datetime + ".py"
    return filename

def open_notepad():
    subprocess.Popen("notepad.exe")

def copy_to_notepad(output):
    filename = get_filename()
    with open(filename, 'w') as out_file:
        out_file.write(output)
    out_file.close()
    subprocess.Popen(["notepad.exe", filename])


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
            open_notepad()
            statement = render_template(current_page) 
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

def voice_assitant_with_output(current_page, output, renderpage):
    try:
        #get voice and fix similar sounding words
        text = convert_word()
        #check if redirection is within the webapp
        within_page, page = redirect_to_app_page(text)
        #return directed page if true
        if within_page == True:
            statement = redirect(page)
        #open notepad if notepad 
        elif ("notepad" in text.lower() or "copy" in text.lower()):
            copy_to_notepad(output)
            statement = renderpage
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
                statement = renderpage
            else:
                flash("Unable to process command")
                statement = renderpage
    except Exception as e:
            flash("No voice or microphone detected")
            statement = renderpage
    return statement   