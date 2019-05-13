import codecs
from enum import Enum

class LookingFor(Enum):
    FOR_DESCRIPTION = 0
    IN_DESCRIPTION = 1
    FOR_INSTANCES = 2
    FOR_FEATURES = 3
    FOR_CLASSES = 4
    FOR_ATRIBUTES = 5
    FOR_HEADER = 6
    IN_HEADER = 7
    CLASS_NAMES = 8

class InfoParser:
    def __init__(self, file, name, path_separator='/'):
        self.file = file
        self.name = name
        self.looking = LookingFor.FOR_DESCRIPTION
        self.latex_code = []
        
    def parse(self):
        self.latex_code.append('\\section{' + self.name + ' dataset}\n\n')
        self.latex_code.append('\\subsection{Apresentao dos Dados}\n\n')
        self.latex_code.append('\\textbf{Nome:} ' + self.name + '\\\\ \\\\\n')
        text = '\\textbf{Descrição:} '

        with open(self.file, 'rt', errors='ignore') as desc_file:
            for line in desc_file:
                if self.looking == LookingFor.FOR_DESCRIPTION \
                    or self.looking == LookingFor.IN_DESCRIPTION:
                    text += self.__parse_description(line)
                    if self.looking == LookingFor.FOR_INSTANCES:
                        text = self.__add_code(text)
                        self.latex_code.append('\\textbf{Objetivo:} \\\\ \n')
                elif self.looking == LookingFor.FOR_INSTANCES:
                    text = '\\textbf{Instâncias:} '
                    text = self.__parse_selection(LookingFor.FOR_FEATURES,
                        text, line, self.__parse_instances)
                elif self.looking == LookingFor.FOR_FEATURES:
                    text = '\\textbf{Número de atributos:} '
                    text = self.__parse_selection(LookingFor.FOR_CLASSES,
                        text, line, self.__parse_features)
                elif self.looking == LookingFor.FOR_CLASSES:
                    text = '\\textbf{Número de classes:} '
                    text = self.__parse_selection(LookingFor.FOR_HEADER, text,
                        line, self.__parse_classes)
                elif self.looking == LookingFor.FOR_HEADER \
                    or self.looking == LookingFor.IN_HEADER:
                    self.__parse_header(line)
        return self.latex_code
                    
    def __parse_selection(self, condicional_lf, text, line, function):
        text += function(line)
        if self.looking == condicional_lf:
            text = self.__add_code(text)
        return text
        
    # parse description
    def __parse_description(self, line):
        if self.looking == LookingFor.FOR_DESCRIPTION \
            and line.startswith('1: Description'):
            self.looking = LookingFor.IN_DESCRIPTION
        elif self.looking == LookingFor.IN_DESCRIPTION:
            if line.startswith('2: Type'):
                self.looking = LookingFor.FOR_INSTANCES
            else:
                return line.replace('\n', '').strip()
        return '' # common return, except when returns line

    def __parse_instances(self, line):
        if line.startswith('4: Instances'):
            self.looking = LookingFor.FOR_FEATURES
            return \
                line.replace('\n', '').replace('4: Instances.', '').strip()
        return ''

    def __parse_features(self, line):
        if line.startswith('5: Features'):
            self.looking = LookingFor.FOR_CLASSES
            return line.replace('\n', '').replace('5: Features.', '').strip()
        return ''

    def __parse_classes(self, line):
        if line.startswith('6: Classes'):
            self.looking = LookingFor.FOR_HEADER
            return line.replace('\n', '').replace('6: Classes.', '').strip()
        return ''

    # add code to the latex_code list, adding linefeed 
    def __add_code(self, text):
        text += '\\\\ \n'
        self.latex_code.append(text)
        return ''

    def __parse_header(self, line):
        if self.looking == LookingFor.FOR_HEADER \
            and line.startswith('8: Header'):
            self.looking = LookingFor.IN_HEADER
        elif line.startswith('@attribute'):
            text = '\\textbf{Atributo - '
            line = line[11:]
            i = line.find(' ')
            text += line[:i] + ':} dado '
            line = line[i+1:]
            if line[0] == '{':
                text += 'categórico, possíveis valores: ('
                values = line.strip()[1:-1].split(',')
                for v in values:
                    text += v.strip() + ', '
                text = text.strip()[:-1] + ')'
            else: # dados numéricos
                text += 'numérico, possíveis valores '
                if line.startswith('real'):
                    text += 'float de '
                else:
                    text += 'inteiro de '
                
                value = line.strip()[line.find('[')+1:-1].split(',')
                text += value[0].strip() + ' a ' + value[1].strip()
                text = text.replace('&', '\&').replace('_', '\_')
            self.__add_code(text)

