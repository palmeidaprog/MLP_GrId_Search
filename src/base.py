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
        
    def scores(self, prediction, y_test, out, e, lr, ls, name, file_id):
        with open(out, 'at') as file:
            second_layer = 0
            if len(ls) > 1:
                second_layer = ls[1]            
            line = f"{file_id}, \"{self.filename} - MLP\","
            line += f"\"Split # {self.iter_n}\","
            line += f"{self.iter_n},{name},{e},{lr},{ls[0]},"
            line += f"{second_layer},"
            line += f"{accuracy_score(y_test, prediction)},"
            line += f"{recall_score(y_test, prediction)},"
            line += f"{precision_score(y_test, prediction)},"
            line += f"{f1_score(y_test, prediction)},"
            line += f"{matthews_corrcoef(y_test, prediction)}\n"
            file.writelines(line)
        pass