import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# read csv files
codeData = pd.read_csv(r'..\codeEIO-data-raw.csv')
codeMethod = pd.read_csv(r'..\codeEIO-method.csv')

# remove duplicate data
print("Original Count: " + str(codeData.shape[0]))
duplicates = codeData.duplicated().sum()
print("Duplicates Found: " + str(duplicates))
codeData = codeData.drop_duplicates()
print("Modified Count: " + str(codeData.shape[0]))

# store unique data into a new csv
codeData.to_csv(r'..\codeEIO-data-clean.csv', index = False, header=True)

# preparation for ML fitting
X = codeData.drop(columns=['Addition', 'Subtraction', 'Multiplication', 'Division', 'Equals'])
y = codeData[['Addition', 'Subtraction', 'Multiplication', 'Division', 'Equals']]

model = DecisionTreeClassifier()
model.fit(X.values, y)

# export and store the trained model and method
pickle.dump(model, open(r'.\FYP_code\saved_codeEIO_model', 'wb'))
pickle.dump(codeMethod, open(r'.\FYP_code\saved_codeEIO_method', 'wb'))