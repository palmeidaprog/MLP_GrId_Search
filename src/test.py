from InfoParser import InfoParser
from Latex import Latex

latex = Latex('teste/teste.tex')
info = InfoParser('../saved_models/adult-names.txt', 'Adult')
code = info.parse()
print(code)
latex.insert_in_file(code)