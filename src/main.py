import warnings
from sklearn.exceptions import DataConversionWarning
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from os import listdir
from DataSet import DataSet
from MLP import MLP

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
folder='../datasets_test/'
output = 'output.csv'
dataset = []

epochs = [10, 50, 100, 500, 5000]
batch = [10, 50, 200]
learning_rate = [0.1, 0.01, 0.001, 0.0001]
layers_n = [1, 2]
layer_size = [10, 50, 100, 500, 1000]
mlp = ""
data = ""

def greed_search(data, dataf, datan):
    print(dataset.X_train)
    print(dataset.y_train)
    for ep in epochs:
        for b in batch:
            for lr in learning_rate:
                for ln in layers_n:
                    for ls in layer_size:
                        mlp = MLP(dataf, datan, i, data, ep, b, lr, ln, ls)
                        mlp.scores(output)
    
for datafile in listdir(folder):
    print(f"##### Opening {datafile} #####")
    output = datafile + '.csv'
    with open(output, 'wt') as out_file: 
        out_file.writelines('\"Descrição\",\"Split #\",\"Epochs\",\"Batch\",\"Learning Rate\",\"Hidden Layers\",\"Nr Perceptrons\",\"Acurácia\",\"F1-Score\",\"Recall\",\"Precisão,MCC\"\n')

    for i in range(5):
        dataset = DataSet(folder + datafile, Normalizer(), random_state=i)
        greed_search(dataset, folder+datafile, datafile)
        dataset = DataSet(folder + datafile, StandardScaler(), random_state=i)
        greed_search(dataset, folder+datafile, datafile)
        
    
    