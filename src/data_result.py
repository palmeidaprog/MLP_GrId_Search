import pandas as pd

data = pd.read_csv('../output/adult_clean/adult.csv')
# data_no_means = pd.DataFrame(data.groupby(['Pre-processing', 'Split RState', 'Epochs', 
#         'Learning Rate', '1st Layer', '2nd Layer', 'Acurácia', 
#         'Precisão', 'Recall','F1-Score',
#         'MCC']))
        # , 'Acurácia', 'Precisão', 'Recall',
        # 'F1-Score', 'MCC' )
data_no_means = data.drop(['File ID', 'Descrição', 'Split #'], axis=1, 
                inplace=False)
data_group = data.groupby(['Pre-processing', 'Epochs', 'Learning Rate', 
        '1st Layer', '2nd Layer']).agg({'Acurácia': "mean", 
        'Precisão': "mean", 'Recall': "mean",'F1-Score': "mean", \
        'MCC': "mean"})


data_no_means  = data_no_means.sort_values(by=['Acurácia','Precisão','Recall'], 
        ascending=False)

data_group  = data_group.sort_values(by=['Acurácia','Precisão','Recall'], 
        ascending=False)
with open('adult_clean_mean.html', 'wt') as f:
    f.writelines(data_group.head().to_html())

with open('adult_clean_no_means.html', 'wt') as f:
    f.writelines(data_no_means.head().to_html())


