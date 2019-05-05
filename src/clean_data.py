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


if not len(argv) > 1:
    print('Please choose a dataset')
    exit()

read_meta(argv[1])
print(names)
pd.set_option('display.max_columns', 30)
df = pd.read_csv(argv[1], names=names, header=i)
#df.columns = names
print(df.head())
print('Colunas: ', end='') 
print(df.columns)

# check for nan and null values
if df.isnull().values.any():
    print('Tnere are NaN and null values. Please treat them')
    exit()

for c in df.columns:
    print(df[c].unique())
    #df[c].value_counts()
    plt.figure()
    plt.title('Distribuição de ' + c)
    #plt.pie(df[c].value_counts() ,labels=df[c].unique())
    plt.bar(df[c].unique(), df[c].value_counts())
    plt.savefig('../output/adult/bar' + c + '.png')
    print(f'saved {c}')
    #plt.df[c].plot(kind='bar')
    


# with open('app.html', 'wt') as file:
#     for line in values.head().to_html():
#         file.writelines(line)
# system('open app.html')


