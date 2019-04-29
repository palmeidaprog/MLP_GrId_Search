import warnings
from sklearn.exceptions import DataConversionWarning
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from os import listdir
from DataSet import DataSet

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
folder='../datasets_test/'
output = 'output.csv'
dataset = []

with open(output, 'wt') as out_file: 
    out_file.writelines('\"Descrição\",\"Acurácia\",\"F1-Score\",\"Recall\",\"Precisão,MCC\"\n')

for datafile in listdir(folder):
    print(f"##### Opening {datafile} #####")
    dataset = DataSet(folder + datafile, Normalizer(), random_state=0)
    print(dataset.X_train)
    print(dataset.y_train)

    

