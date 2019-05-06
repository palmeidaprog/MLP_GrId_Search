# Paulo R. Almeida Filho
# <pauloalmeidaf@gmail.com>
# http://www.github.com/palmeidaprog

import requests
from os import path, makedirs
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, Normalizer, LabelEncoder
from joblib import dump, load
from DatasetType import DatasetType

# read datasets, preprocesses and split it using pandas.DataFrame
class DataSet:
    # validation_size = % of the train_size that is saved for validation
    # file(str) = name of file to be opened
    # preproc = Preprocessor, usually Normalizer or Standard Scaler
    # random_state = train_test_split 's random_state parameter
    # train_size, test_size = train_test_split's parameters
    # validation_size = portion of train data wich will be saved for 
    #                   validation
    # save_folder = location to save the output data
    # dataset_type = KEEL, TREATED_DATA_JOBLIB, COMMON_CSV, 
    def __init__(self, file, preproc=Normalizer(), random_state=0, 
            train_size=0.75, validation_size=0.1, test_size=0.25, 
            save_folder='../output/', dataset_type=DatasetType.KEEL):
        self.file = file
        self.train_size=train_size
        self.test_size = test_size
        self.validation_size = validation_size
        self.preproc = preproc
        self.random_state = random_state
        self.save_folder = save_folder
        self.dataset_type = dataset_type
        self.__split_data()
    
    # .dat KEEL/UCI with @ meta info on header specific
    def __read_meta(self):
        self.i = 0
        self.names = []
        self.name = ""
        with open(self.file, 'rt') as in_file:
            for line in in_file:
                self.i += 1
                if line.startswith("@relation"):
                    self.name = line.split(" ")[1].replace('\n', '')
                if line.startswith("@inputs"):
                    for n in line.split(" "):
                        if n != "@inputs":
                            self.names.append(n.replace('\n', ""))
                if line.startswith("@data"):
                    break
        self.names.append("Class")
        pass    

    # core method of the class, where the magic happens 
    def __split_data(self):
        if self.dataset_type == DatasetType.KEEL:
            self.__read_meta()
            data = pd.read_csv(self.file, names=self.names, \
                header=self.i)
        elif self.dataset_type == DatasetType.COMMON_CSV:
            data = pd.read_csv(self.file)
        elif self.dataset_type == DatasetType.TREATED_DATA_JOBLIB:
            data = load(self.file)
            self.names = data.columns
            self.name = self.file.split('/')[-1].split('.')[0]
        
        # pre processing data
        data = data.apply(LabelEncoder().fit_transform)
        y = data['Class']
        X = data.drop('Class', axis=1)
        c = X.columns
        X = pd.DataFrame(self.preproc.fit_transform(X))
        X.columns = c
    
        # Data split
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, stratify=y, 
            train_size=self.train_size, test_size=(1.0 - self.train_size),
            random_state=self.random_state)
        
        # validation split
        if self.validation_size > 0:
            self.X_train, self.X_validation, self.y_train, self.y_validation \
                = train_test_split(self.X_train, self.y_train, 
                stratify=self.y_train, 
                train_size=(1.0 - self.validation_size),
                test_size=self.validation_size, 
                random_state=self.random_state)
            self.__saveXY(self.X_validation, 'X_validation')
            self.__saveXY(self.y_validation, 'y_validation')
            
        self.__saveXY(self.X_train, 'X_train')
        self.__saveXY(self.X_test, 'X_test')
        self.__saveXY(self.y_train, 'y_train')
        self.__saveXY(self.y_test, 'y_test')
        
    # save with joblib
    def __saveData(self, dataSplit, name):
        save_filename = self.file.split('/')[-1].split('.')[0] + '_' + \
            name + '_random_state' + str(self.random_state)
        dump(dataSplit, self.save_folder + save_filename + '.joblib')

    # save the splits inside a csv
    def __saveXY(self, d, name):
        csvfile = name + '_rs_' + str(self.random_state) + '.csv'
        # add a bar at the end of save_folder to concatenate
        if self.save_folder[-1] != '/':
            self.save_folder.append('/')
        # create a folder specific with the dataset name inside output folder
        if not self.save_folder.endswith(self.name + '/'):
            self.save_folder += self.name + '/'
        # if the output folder doesn't exists creates one
        if not path.isdir(self.save_folder):
            makedirs(self.save_folder)
        # save the file
        pd.DataFrame(d).to_csv(self.save_folder + csvfile)

