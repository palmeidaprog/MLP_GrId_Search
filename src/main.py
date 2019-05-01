import warnings 
from sklearn.exceptions import DataConversionWarning
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from os import listdir
from os import mkdir
from MLP import MLP
from DataSet import DataSet


warnings.filterwarnings(action='ignore', category=Warning)
folder='../datasets_test/'
output_folder = '../output/'
save_folder = '../saved_models/'
output = 'output.csv'
dataset = []
progress = 0.0

epochs = [10, 50, 100, 500, 5000]
batch = [10, 50, 200]
learning_rate = [0.1, 0.01, 0.001, 0.0001]
tuples = [(10,), (50,), (100,), (500,), (1000,)]
layer_size = [10, 50, 100, 500, 1000]
mlp = ""
data = ""
file_id = 1000

def generate_tuples():
    for i in layer_size:
        for j in layer_size:
            tuples.append((i, j))
    
# data = DataSet
# dataf = Data
def grid_search(data, dataf, datan, preprocess):
    global progress
    global file_id
    for ep in epochs:
        for b in batch:
            for lr in learning_rate:
                for ls in tuples:
                    mlp = MLP(dataf, datan, i, data, ep, b, lr, ls, 
                        preprocess, file_id, save_folder)
                    file_id += 1
                    mlp.scores(output)
                    progress += 0.004
                    print('\r%s - Progress: %.2lf %%' % (data.file, 
                        progress), end='', flush=True)

# main code
generate_tuples()
for datafile in listdir(folder):
    if not datafile.endswith('.dat'):
        continue
    print(f"##### Opening {datafile} #####")
    output = output_folder + datafile.split('.')[0] + '.csv'
    #mkdir(output_folder)
    with open(output, 'wt') as out_file: 
        out_file.writelines('\"File ID\", \"Descrição\",\"Split #\",' +
            '\"Pre-processing\"' +
            '\"Split RState\",\"Epochs\",\"Batch\",\"Learning Rate\",' +
            '\"1st Layer\",\"2nd Layer\",' + \
            '"\"Acurácia\",\"F1-Score\",\"Recall\",\"Precisão,MCC\"\n')

    for i in range(5):
        dataset = DataSet(folder + datafile, Normalizer(), random_state=i)
        grid_search(dataset, folder+datafile, datafile, 'Normalizer')
        dataset = DataSet(folder + datafile, StandardScaler(), random_state=i)
        grid_search(dataset, folder+datafile, datafile, 'Standard Scaler')
    print('\r%s - Progress: 100.00%%' % dataset.file)
    
