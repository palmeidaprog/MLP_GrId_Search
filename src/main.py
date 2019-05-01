import warnings 
from sklearn.exceptions import DataConversionWarning
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from os import listdir
from os import mkdir
from DataSet import DataSet
from MLP import MLP

warnings.filterwarnings(action='ignore', category=Warning)
folder='../datasets_test/'
output_folder = '../output/'
output = 'output.csv'
dataset = []

epochs = [10, 50, 100, 500, 5000]
batch = [10, 50, 200]
learning_rate = [0.1, 0.01, 0.001, 0.0001]
tuples = [(10,), (50,), (100,), (500,), (1000,)]
layer_size = [10, 50, 100, 500, 1000]
mlp = ""
data = ""

def generate_tuples():
    for i in layer_size:
        for j in layer_size:
            tuples.append((i, j))
    

# data = DataSet
# dataf = Data
def grid_search(data, dataf, datan):
    #print(dataset.X_train)
    #print(dataset.y_train)
    progress = 0.0
    for ep in epochs:
        for b in batch:
            for lr in learning_rate:
                for ls in tuples:
                    mlp = MLP(dataf, datan, i, data, ep, b, lr, ls)
                    mlp.scores(output)
                    progress += 0.004
                    print('\r%s - Progress: %.2lf %%' % (data.file, 
                        progress), end='', flush=True)
    print('\r%s - Progress: 100.00%' % (data.file), end='', flush=True)

# main code
generate_tuples()
for datafile in listdir(folder):
    if not datafile.endswith('.dat'):
        continue
    print(f"##### Opening {datafile} #####")
    output = output_folder + datafile.split('.')[0] + '.csv'
    #mkdir(output_folder)
    with open(output, 'wt') as out_file: 
        out_file.writelines('\"Descrição\",\"Split #\",\"Epochs\",\"Batch\"" \
            + ",\"Learning Rate\",\"1st Layer\",\"2nd Layer\"," + \
            "\"Acurácia\",\"F1-Score\",\"Recall\",\"Precisão,MCC\"\n')

    for i in range(5):
        dataset = DataSet(folder + datafile, Normalizer(), random_state=i)
        grid_search(dataset, folder+datafile, datafile)
        dataset = DataSet(folder + datafile, StandardScaler(), random_state=i)
        grid_search(dataset, folder+datafile, datafile)
