from warnings import filterwarnings
from sys import argv
from joblib import dump
from MLP import MLP
from sklearn.preprocessing import Normalizer, StandardScaler
from DataSet import DataSet
import eli5
from eli5.sklearn import PermutationImportance
from IPython.display import display, HTML


filterwarnings(action='ignore')
if len(argv) != 9:
    print('USAGE: python explainability.py <file_name> ' + \
        '<split_random_state> <preprocessing> <epochs> <batch> ' + \
        '<learning_rate> <1st layer> <2nd layer>')
    print('\nPreprocessing: \t0 for Normalizaer\n\t\t1 for Standard Scaler')
    print('Choose 0 for 2nd Layer to have a single hidden layer')
else:
    prep = Normalizer()
    if argv[3] == 1:
        prep = StandardScaler()

    layers = ''
    if int(argv[8]) == 0:
        layers = (int(argv[7]),)
    else:
        layers = (int(argv[7]), int(argv[8]))

    data = DataSet(argv[1], preproc=prep, validation_size=0.1, 
            random_state=int(argv[2]))
    mlp = MLP(argv[1], argv[1], int(argv[2]), data, int(argv[4]), 
            int(argv[5]), float(argv[6]), layers, 'Standard Scaler', 0, 
            save_folder='./')
    
    perm = PermutationImportance(mlp.clf, random_state=data.random_state)
    perm.fit(data.X_validation, data.y_validation)
    #print(data.names[0:len(data.names) - 1])
    #print(list(data.X_validation))
    with open(argv[1].split('/')[-1].split('.')[0] + '_clf.html', 'wt') as ff:
         ff.write(eli5.show_weights(perm, feature_names = data.names[0:len(data.names) - 1]).data) 
    dump(eli5.show_weights(perm, feature_names = data.names[0:len(data.names) - 1]).data, 'x.html')
    #eli5.show_prediction(perm, feature_names = data.names[0:len(data.names) - 1])
    save_file = argv[1].split('/')[-1].split('.')[0] + '_model.joblib'
    dump(mlp.clf, save_file)


