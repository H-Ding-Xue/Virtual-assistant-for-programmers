import pandas as pd
import random

value1 = []
value2 = []
value3 = []
result = []
addition = []
subtraction = []
multiplication = []
division = []
equals = []

mathDict = {
    "+": "Addition",
    "-": "Subtraction",
    "*": "Multiplication",
    "/": "Division"
}

counter = 0

def appendAddition():
    addition.append(1)
    subtraction.append(0)
    multiplication.append(0)
    division.append(0)
    equals.append(0)

def appendSubtraction():
    addition.append(0)
    subtraction.append(1)
    multiplication.append(0)
    division.append(0)
    equals.append(0)

def appendMultiplication():
    addition.append(0)
    subtraction.append(0)
    multiplication.append(1)
    division.append(0)
    equals.append(0)

def appendDivision():
    addition.append(0)
    subtraction.append(0)
    multiplication.append(0)
    division.append(1)
    equals.append(0)

def appendEquals():
    addition.append(0)
    subtraction.append(0)
    multiplication.append(0)
    division.append(0)
    equals.append(1)

def randThree(min, max, count):
    global counter
    for i in range(count):
        a = random.randint(min, max)
        b = random.randint(min, max)
        c = random.randint(min, max)
        symbol1, eng1 = random.choice(list(mathDict.items()))
        symbol2, eng2 = random.choice(list(mathDict.items()))

        if a == 0 or b == 0 or c == 0:
            continue
        
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
        print("randThree(" + str(min) + ", " + str(max) + "): " + str(counter))

def randTwo(min, max, count):
    global counter
    for i in range(count):
        a = random.randint(min, max)
        b = random.randint(min, max)
        c = 0
        symbol1, eng1 = random.choice(list(mathDict.items()))

        if a == 0 or b == 0:
            continue

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
        print("randTwo(" + str(min) + ", " + str(max) + "): " + str(counter))
        
def randOne(min, max, count):
    global counter
    for i in range(count):
        a = random.randint(min, max)
        b = 0
        c = 0

        answer = a
        value1.append(a)
        value2.append(b)
        value3.append(c)
        result.append(answer)
        appendEquals()
        counter += 1
        print("randOne(" + str(min) + ", " + str(max) + "): " + str(counter))

def generator(min, max, count):
    randThree(min, max, count)
    randTwo(min, max, count)
    randOne(min, max, count)

# generate range 0 to 1000 with 2.5 millions raw data
generator(0, 1001, 2500000)

data = {'Value1': value1,
        'Value2': value2,
        'Value3': value3,
        'Result': result,
        'Addition': addition,
        'Subtraction': subtraction,
        'Multiplication': multiplication,
        'Division': division,
        'Equals': equals
}

# export into csv
df = pd.DataFrame(data, columns = ['Value1', 'Value2', 'Value3', 'Result', 'Addition', 'Subtraction', 'Multiplication', 'Division', 'Equals'])
df.to_csv(r'..\codeEIO-data-raw.csv', index = False, header = True)

print("Total data input: " + str(counter))