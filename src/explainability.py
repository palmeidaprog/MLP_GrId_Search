from warnings import filterwarnings
from sys import argv, exit
from joblib import dump
from MLP import MLP
from sklearn.preprocessing import Normalizer, StandardScaler
from DataSet import DataSet
import eli5
from eli5.sklearn import PermutationImportance
from IPython.display import display, HTML
from DatasetType import DatasetType
import pandas as pd
import lime
from lime.lime_tabular import LimeTabularExplainer

filterwarnings(action='ignore')
pd.set_option('display.max_columns', 30)
if len(argv) != 8:
    print('USAGE: python explainability.py <file_name> ' + \
        '<split_random_state> <preprocessing> <epochs> ' + \
        '<learning_rate> <1st layer> <2nd layer>')
    print('\nPreprocessing: \t0 for Normalizaer\n\t\t1 for Standard Scaler')
    print('Choose 0 for 2nd Layer to have a single hidden layer')
else:
    prep = Normalizer()
    if int(argv[3]) == 1:
        prep = StandardScaler()

    layers = ''
    if int(argv[7]) == 0:
        layers = (int(argv[6]),)
    else:
        layers = (int(argv[6]), int(argv[7]))
    name = argv[1].split('/')[-1].split('.')[0]

    dt = DatasetType.TREATED_DATA_JOBLIB
    
    categorical_columns = ['Workclass', 'Education', 'Marital-status', 
             'Occupation', 'Relationship', 'Race', 'Sex', 'Native-country', 
             'Class']
    data = DataSet(argv[1], preproc=prep, validation_size=0.1, 
            random_state=int(argv[2]), 
            dataset_type=dt, categorical_columns=categorical_columns)
    
    mlp = MLP(argv[1], argv[1], int(argv[2]), data, int(argv[4]), 
            float(argv[5]), layers, 'Standard Scaler', 0, 
            save_folder='./')
    
    perm = PermutationImportance(mlp.clf, random_state=data.random_state)
    perm.fit(data.X_validation, data.y_validation)
    print(type(data.X_validation))
    #print(data.names[0:len(data.names) - 1])
    #print(list(data.X_validation))
    with open(name + '_show_wght.html', 'wt') as ht:
        ht.writelines(eli5.show_weights(mlp.clf, vec='bow', 
                feature_names=list(data.X_train.columns)).data)

    with open(name + '_clf.html', 'wt') as ff:
        ff.writelines(eli5.show_weights(perm, 
            feature_names=list(data.X_train.columns)).data) 

    
            # , feature_names=list(data.X_train.columns)
            # training_labels=data.X_train['Age'],

    d = pd.DataFrame()
    for c in range(len(data.categorical_columns)):
        s = data.categorical_columns[c]
        #d = pd.DataFrame(data.encoder[c].classes_)
        d = pd.concat([d, pd.DataFrame(data.encoder[c].classes_)], axis=1)
        
        # d.columns = data.categorical_columns
            # f = list(data.encoder[c].classes_).to_html()
            
            # save_to_file(d.to_html(), data.name + '_' + s + '_legend.png')
            # with open(data.name + '_' + s + '_legend.html', 'wt') as ht:
            #     ht.writelines(d.to_html())
        # for c in range(len(data.encoder)):
        #     s = data.categorical_columns[c]
        #     if s == 'Class':
        #         continue
        #     X_test[s] = data.encoder[c].inverse_trans
    d.columns = data.categorical_columns
    d = d.fillna('-')
    with open(data.name + '_legend.html', 'wt') as ht:
        ht.writelines(d.to_latex())

    # asking for explanation for LIME modela
    for i in range(5):
        id = 10 + i
        X_test = data.X_test

        # print(data.X_test.head())

        # print(data.categorical_columns)
        # print(data.X_test['Workclass'])
        s = data.categorical_columns[0]
        # print(data.X_test[s])


        # d = pd.DataFrame()
        # for c in range(len(data.categorical_columns)):
        #     s = data.categorical_columns[c]
        #     #d = pd.DataFrame(data.encoder[c].classes_)
        #     d = pd.concat([d, pd.DataFrame(data.encoder[c].classes_)], axis=1)
            # d.columns = data.categorical_columns
            # f = list(data.encoder[c].classes_).to_html()
            
            # save_to_file(d.to_html(), data.name + '_' + s + '_legend.png')
            # with open(data.name + '_' + s + '_legend.html', 'wt') as ht:
            #     ht.writelines(d.to_html())
        # for c in range(len(data.encoder)):
        #     s = data.categorical_columns[c]
        #     if s == 'Class':
        #         continue
        #     X_test[s] = data.encoder[c].inverse_transform(X_test[s])

        
        with open(name + '_' + str(id) + '.html', 'wt') as l10:
            l10.writelines(data.X_test.iloc[[id]].to_html())

        explainer = LimeTabularExplainer(data.X_train.values, 
            feature_names=list(data.X_train.columns), 
            class_names=['<=50K', '>50K'])

        exp = explainer.explain_instance(data.X_test.values[id], 
            mlp.clf.predict_proba, num_features=len(data.X_train.columns))
        
        exp.show_in_notebook()
        exp.save_to_file(name + '_' + str(id) + '_explanation.html')

        exp.as_pyplot_figure()
        from matplotlib import pyplot as plt
        plt.tight_layout()
        plt.savefig(name + '_' + str(id) + '_explanation_plot.png')
        
    #eli5.show_weights(perm, feature_names = data.names[0:len(data.names) - 1])
    #eli5.show_prediction(perm, feature_names = data.names[0:len(data.names) - 1])