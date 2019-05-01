from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import matthews_corrcoef

class Base:
    def __init__(self, file, filename, i):
        self.file = file
        self.iter_n = i
        self.filename = filename
        
    def scores(self, prediction, y_test, out, e, b, lr, ln, ls):
        with open(out, 'at') as file:
            line = f"\"{self.filename} - MLP\","
            line += f"\"Split # {self.iter_n}\","
            line += f"{e},{b},{lr},{ln},{ls},"
            line += f"{accuracy_score(y_test, prediction)},"
            line += f"{matthews_corrcoef(y_test, prediction)},"
            line += f"{f1_score(y_test, prediction,average='macro')},"
            line += f"{recall_score(y_test, prediction, average='macro')},"
            line += f"{precision_score(y_test, prediction, average='macro')}\n"
            file.writelines(line)
            #print(f"{classification_report(self.treated_data.target_test, self.prediction)}")
        pass