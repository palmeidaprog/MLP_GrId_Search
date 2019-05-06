from sys import argv, exit
import pandas as pd
from joblib import dump
from os import system
from matplotlib import pyplot as plt
import sys


names = []
name = ''
i = 0

def read_meta(file):
    global i
    global name
    global names
    with open(file, 'rt') as in_file:
        for line in in_file:
            i += 1
            if line.startswith("@relation"):
                name = line.split(" ")[1]
            if line.startswith("@inputs"):
                for n in line.split(" "):
                    if n != "@inputs":
                        names.append(n.replace('\n', "").replace(',',''))
            if line.startswith("@data"):
                break
    names.append("Class")

ds = ''
if not len(argv) > 1:
    ds = '../datasets/adult.dat'
else:
    ds = argv[1]

read_meta(ds)
print(names)
pd.set_option('display.max_columns', 30)
df = pd.read_csv(ds, names=names, header=i)
#df.columns = names
print(df.head())
print('Colunas: ', end='') 
print(df.columns)

# with open('../output/adult/adult.html', 'wt') as f:
#     f.writelines(df.describe().to_html())
print(df.shape[0])

# check for nan and null values
if df.isnull().values.any():
    print('Tnere are NaN and null values. Please treat them')
    exit()

#i = 0
#for c in df.columns:
    #i += 1
    #print(df[c].unique())
total = df.shape[0]
#cg = df['Capital-gain'].value_counts().columns
#cl = df['Capital-loss'].value_counts().columns
print(df['Capital-loss'].value_counts())
print(df['Capital-gain'].value_counts())
print(f'Cg: {100 * 43081 / total}')
print(f'Cl: {100 * 41431 / total}')
print(df.shape[0])

df.drop('Capital-loss', axis=1, inplace=True)
df.drop('Capital-gain', axis=1, inplace=True)

#corrigir valores
df.Age.astype(float)
df['Education-num'].astype(float)
df['Hours-per-week'].astype(float)
df['Fnlwgt'].astype(float)

dump(df, '../clean_data/adult.joblib')

    # plt.figure()
    # plt.title('Distribuição de ' + c)
    # #plt.pie(df[c].value_counts() ,labels=df[c].unique())
    # plt.bar(df[c].unique(), df[c].value_counts())
    # plt.savefig('../output/adult/bar_' + c + '.png')
    # plt.close()
    
    # plt.figure()
    # plt.title('Distribuição de ' + c)
    # plt.pie(df[c].value_counts(), labels=df[c].unique())
    # plt.savefig('../output/adult/pie_' + c + '.png')
    # plt.close()
    # print(df.shape[0])
    # print(f'saved {c}')
    # print(str(i) + '/' + str(df.shape[1]))
    


# with open('app.html', 'wt') as file:
#     for line in values.head().to_html():
#         file.writelines(line)
# system('open app.html')


