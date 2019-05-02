
import requests
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer, LabelEncoder
from joblib import dump, load

class DataSet:
    # validation_size = % of the train_size that is saved for validation
    def __init__(self, file, preproc=Normalizer(), random_state=0, 
            train_size=0.75, validation_size=0, test_size=0.25, 
            save_folder='../saved_models/'):
        self.file = file
        self.train_size=train_size
        self.test_size = test_size
        self.validation_size = validation_size
        self.preproc = preproc
        self.random_state = random_state
        self.save_folder = save_folder
        self.__split_data()
        
    def __read_meta(self):
        self.i = 0
        self.names = []
        self.name = ""
        with open(self.file, 'rt') as in_file:
            for line in in_file:
                self.i += 1
                if line.startswith("@relation"):
                    self.name = line.split(" ")[1]
                if line.startswith("@inputs"):
                    for n in line.split(" "):
                        if n != "@inputs":
                            self.names.append(n.replace('\n', ""))
                if line.startswith("@data"):
                    break
        self.names.append("Class")
        pass    

    def __split_data(self):
        self.__read_meta()
        
        print(self.file)
        data = pd.read_csv(self.file, names=self.names, \
            header=self.i)
        last_col = len(self.names) - 1
        X = data.iloc[:, 0:last_col]
        y = data.iloc[:, last_col].values
    
        X = X.apply(LabelEncoder().fit_transform)
        #X = LabelEncoder().fit_transform
        X = self.preproc.fit_transform(X)
        
        # Data split
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, stratify=y, 
            train_size=self.train_size, test_size=(1.0 - self.train_size),
            random_state=self.random_state)
        #self.__saveData(self.X_test, 'X_test')
        #self.__saveData(self.y_test, 'y_test')
        
        # validation split
        if self.validation_size > 0:
            self.X_train, self.X_validation, self.y_train, self.y_validation \
                = train_test_split(self.X_train, self.y_train, 
                stratify=self.y_train, 
                train_size=(1.0 - self.validation_size),
                test_size=self.validation_size, 
                random_state=self.random_state)
            #self.__saveData(self.X_validation, 'X_validation')
            #self.__saveData(self.y_validation, 'y_validation')

        #self.__saveData(self.X_train, 'X_train')
        #self.__saveData(self.y_train, 'y_train')

    def __saveData(self, dataSplit, name):
        save_filename = self.file.split('/')[-1].split('.')[0] + '_' + \
            name + '_random_state' + str(self.random_state)
        dump(dataSplit, self.save_folder + save_filename + '.joblib')
