
import requests
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
#from TreatedData import TreatedData
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer

class DataSet:
    # validation_size = % of the train_size that is saved for validation
    def __init__(self, file=None, preproc=Normalizer(), random_state=0, 
            train_size=0.75, validation_size=0.1, test_size=0.25):
        self.file = file
        self.train_size=train_size
        self.test_size = test_size
        self.validation_size = validation_size
        self.preproc = preproc
        self.random_state = random_state
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
        
        data = pd.read_csv(self.file, names=self.names, \
            header=self.i)
        last_col = len(self.names) - 1
        X = data.iloc[:, 0:last_col]
        y = data.iloc[:, last_col]
    
        X = X.apply(LabelEncoder().fit_transform)
        #X = LabelEncoder().fit_transform
        X = self.preproc.fit_transform(X)
        
        # Data split
        self.X_train, self.X_test, self.y_train, self.test = \
            train_test_split(X, y, stratify=y, 
            train_size=self.train_size, test_size=(1.0 - self.train_size),
            random_state=self.random_state)
        
        self.X_train, self.X_validation, self.y_train, self.y_validation = \
            train_test_split(self.X_train, self.y_train, 
            stratify=self.y_train, train_size=(1.0 - self.validation_size),
            test_size=self.validation_size, random_state=self.random_state)

        
        # std_data = TreatedData(self.names, s.fit_transform(self.ft_train), 
        #     s.transform(self.ft_test), self.tg_train, self.tg_test)



        #data = data.apply(le.fit_transform)
        # ft = self.data.iloc[:, 0:last_col].values
        # ft.apply(le.fit_transform)
        # tg = self.data.iloc[:, last_col].values
        # with open('targets.txt', 'wt') as file:
        #     print(tg, file=file)
        
        # kfold = KFold(10, True)
        # for train, test in kfold.split(ft, y=tg):
        #     continue
            
        # with open("train.txt", 'wt') as file:
        #     print(ft[train], file=file)
        # with open('test.txt', 'wt') as file:
        #     print(ft[test], file=file)
        # self.ft_train = ft[train]
        # self.ft_test = ft[test]
        # self.tg_train = tg[train]
        # self.tg_test = tg[test]
        # self.ft_train, self.ft_test, self.tg_train, self.tg_test = \
        #     train_test_split(ft, tg, test_size=self.test_size, 
        #     train_size=self.train_size, random_state=0)
        # pass

    # def __unzip(self, file):
        #     to_unzip = zipfile.ZipFile(file, 'r')
        #     to_unzip.extractall()
        #     to_unzip.close()
        #     os.remove(file)
        #     self.file = file.split('.')[0] + '.dat'
        #     pass

    # def download(self):
    #     response = requests.get(self.url, allow_redirects=True)
    #     open(self.url.split('/')[-1], 'wb').write(response.content)
        
    #     if self.url.endswith('.zip'):
    #         self.__unzip(self.url.split('/')[-1])

    
    # def extract_data(self):
    #     if self.url != None:
    #         self.download()    
    #     self.__read_meta()
    #     self.data = pd.read_csv(self.file, names=self.names, \
    #         header=self.i)
    #     #__read_data() 


