from warnings import filterwarnings
from sklearn.exceptions import DataConversionWarning
from sklearn.preprocessing import Normalizer, StandardScaler
from os import listdir, mkdir, path
from MLP import MLP
from DataSet import DataSet
from sys import argv, exit
from DatasetType import DatasetType

filterwarnings(action='ignore')
folder='../datasets_test/'
save_folder = '../saved_models/'
output = 'output.csv'
dataset = []
epochs = [50, 100, 500]
learning_rate = [0.01, 0.001]
layer_size = [(10,), (50,), (100,), (10, 10), (50, 10), (100, 10)]
mlp = ''
data = ''
file_id = 1000
progress = 0.0

# data = DataSet
# dataf = Data

def calculate_percentage():
    return 100 / (10 * len(epochs) * len(learning_rate) * len(layer_size))

def grid_search(data, dataf, datan, preprocess, progress_inc):
    global progress
    global file_id
    for ep in epochs:
        for lr in learning_rate:
            for ls in layer_size:
                mlp = MLP(dataf, datan, i, data, ep, lr, ls, preprocess, 
                    file_id, save_folder)
                file_id += 1
                mlp.scores(output)
                progress += progress_inc
                if progress >= 100:
                    progress = 100
                print('\r%s - Progress: %.2lf %%' % (data.file, 
                    progress), end='', flush=True)

def early_exit(msg):
    print(msg)
    print("Usage: python main.py [file_name or dir_name] [optional = " + \
            "output folder]")
    exit()
    
# main code
progress_inc = calculate_percentage()
file_list = []

# checking arguments
if len(argv) < 2:
    early_exit('You need to provide a dataset or a folder')
elif path.isfile(argv[1]):
    file = argv[1].split('/')[-1]
    file_list.append(file)
    folder = argv[1].replace(file, '')
elif path.isdir(argv[1]):
    file_list = listdir(folder)
else:
    early_exit(f"{argv[1]} doesn't exist")

if len(argv) == 2:
    output_folder = '../output/'
else:
    output_folder = argv[2]
    if output_folder[-1] != '/':
        output_folder += '/'
    if path.isfile(output_folder):
        early_exit(f"{argv[2]} is not a directory")
    elif not path.isdir(output_folder):
        mkdir(output_folder)

for datafile in file_list:
    dataset_type = DatasetType.COMMON_CSV
    if datafile.endswith('.dat'):
        dataset_type = DatasetType.KEEL
    elif datafile.endswith('.joblib'): 
        dataset_type = DatasetType.TREATED_DATA_JOBLIB
    else:    
        continue
        
    print(f"##### Opening {datafile} #####")
    output = output_folder + datafile.split('.')[0] + '.csv'
    print(output)
    with open(output, 'wt') as out_file: 
        out_file.writelines('\"File ID\",\"Descrição\",\"Split #\",' +
            '\"Split RState\",' +
            '\"Pre-processing\",\"Epochs\",\"Learning Rate\",' +
            '\"1st Layer\",\"2nd Layer\",' + \
            '\"Acurácia\",\"Recall\",\"Precisão\",\"F1-Score\",\"MCC\"\n')
    
    progress = 0.0
    for i in range(5):
        dataset = DataSet(folder+datafile, Normalizer(), validation_size=0.1, 
                random_state=i, dataset_type=dataset_type)
        grid_search(dataset, folder+datafile, datafile, 'Normalizer', 
                progress_inc)
        dataset = DataSet(folder + datafile, StandardScaler(), 
                validation_size=0.1, random_state=i, 
                dataset_type=dataset_type)
        grid_search(dataset, folder+datafile, datafile, 'Standard Scaler',
                progress_inc)
    print('\r%s - Progress: 100.00%%' % dataset.file)