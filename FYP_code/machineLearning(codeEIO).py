import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
import pickle

# generate random data
def generateData(min, max, count, createCSV):
    print("Begin generating raw data..")
    value1 = []
    value2 = []
    value3 = []
    result = []
    addition = []
    subtraction = []
    multiplication = []
    division = []
    counter = 0

    mathDict = {
        "+": "Addition",
        "-": "Subtraction",
        "*": "Multiplication",
        "/": "Division"
    }

    # simulate one-hot-encoding
    def appendAddition():
        addition.append(1)
        subtraction.append(0)
        multiplication.append(0)
        division.append(0)

    def appendSubtraction():
        addition.append(0)
        subtraction.append(1)
        multiplication.append(0)
        division.append(0)

    def appendMultiplication():
        addition.append(0)
        subtraction.append(0)
        multiplication.append(1)
        division.append(0)

    def appendDivision():
        addition.append(0)
        subtraction.append(0)
        multiplication.append(0)
        division.append(1)

    # generate 3 random values
    for i in range(count):
        a = random.randint(min, max)
        b = random.randint(min, max)
        c = random.randint(min, max)
        symbol1, eng1 = random.choice(list(mathDict.items()))
        symbol2, eng2 = random.choice(list(mathDict.items()))
            
        answer = eval(str(a) + symbol1 + str(b) + symbol2 + str(c))
        value1.append(a)
        value2.append(b)
        value3.append(c)
        result.append(answer)
        if eng1 == 'Addition':
            appendAddition()
        elif eng1 == 'Subtraction':
            appendSubtraction()
        elif eng1 == 'Multiplication':
            appendMultiplication()
        elif eng1 == 'Division':
            appendDivision()

        if eng2 == 'Addition':
            addition[counter] += 1
        elif eng2 == 'Subtraction':
            subtraction[counter] += 1
        elif eng2 == 'Multiplication':
            multiplication[counter] += 1
        elif eng2 == 'Division':
            division[counter] += 1
        counter += 1

    # generate 2 random values
    for i in range(count):
        a = random.randint(min, max)
        b = random.randint(min, max)
        c = 0
        symbol1, eng1 = random.choice(list(mathDict.items()))

        answer = eval(str(a) + symbol1 + str(b))
        value1.append(a)
        value2.append(b)
        value3.append(c)
        result.append(answer)
        if eng1 == 'Addition':
            appendAddition()
        elif eng1 == 'Subtraction':
            appendSubtraction()
        elif eng1 == 'Multiplication':
            appendMultiplication()
        elif eng1 == 'Division':
            appendDivision()
        counter += 1
    
    print("Total raw data count: " + str(counter))
    data = {'Value1': value1,
            'Value2': value2,
            'Value3': value3,
            'Result': result,
            'Addition': addition,
            'Subtraction': subtraction,
            'Multiplication': multiplication,
            'Division': division
    }
    # convert data into dataframe
    print("Converting to dataframe..")
    df = pd.DataFrame(data, columns = ['Value1', 'Value2', 'Value3', 'Result', 'Addition', 'Subtraction', 'Multiplication', 'Division'])

    if createCSV == True:
        # export raw data into csv
        # will be stored in a directory above the current folder
        print("Exporting raw data to csv file..")
        df.to_csv(r'..\codeEIO-data-raw.csv', index = False, header = True)
    print("Completed generating raw data")
    return df


# training ML model
def trainModel(df, createCSV):
    print("Begin training model..")
    # read csv files
    CodeMtd = pd.read_csv(r'.\codeEIO-method.csv')
    
    # remove duplicate data
    print("Original Count: " + str(df.shape[0]))
    duplicates = df.duplicated().sum()
    print("Duplicates Found: " + str(duplicates))
    df = df.drop_duplicates()
    print("Modified Count: " + str(df.shape[0]))

    if createCSV == True:
        # store unique data into a new csv
        # will be stored in a directory above the current folder
        print("Exporting clean data to csv file..")
        df.to_csv(r'..\codeEIO-data-clean.csv', index = False, header=True)

    # preparation for ML fitting
    X = df.drop(columns=['Addition', 'Subtraction', 'Multiplication', 'Division'])
    y = df[['Addition', 'Subtraction', 'Multiplication', 'Division']]

    model = DecisionTreeClassifier()
    model.fit(X.values, y)
    
    # export and store the trained model and method
    print("Exporting to pickle file..")
    pickle.dump(model, open(r'.\FYP_code\saved_codeEIO_model', 'wb'))
    pickle.dump(CodeMtd, open(r'.\FYP_code\saved_codeEIO_method', 'wb'))
    print("Completed training model")


####################################################################################################
# configuration
####################################################################################################
# generate random values between min & max values (inclusive)
minValue = 1
maxValue = 1000
# no. of raw data to generate (may include duplicates)
count = 50000000
# set True to create csv file
createCSV = True

df = generateData(minValue, maxValue, count, createCSV)
trainModel(df, createCSV)