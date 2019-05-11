import codecs
import os
from os.path import isfile, isdir, pardir
from enum import Enum

abnt_default = [
    '\\documentclass[12pt,a4paper]{article}\n',
    '\\usepackage[T1]{fontenc}\n',
    '\\usepackage{graphicx}\n',
    '\\usepackage{times}\n',
    '\\graphicspath{ {pictures/} }\n',
    '%\\usepackage{xcolor}\n',
    '\\usepackage[formats]{listings}\n',
    '\\setlength{\\parindent}{0pt}\n',
    '%\\usepackage[latin1]{inputenc}\n',
    '\\usepackage[margin=0.7in]{geometry}\n',
    '\\usepackage{amsmath}\n',
    '\\usepackage{amsfonts}\n',
    '\\providecommand{\\sin}{} \\renewcommand{\\sin}{\\hspace{2pt}\\mathrm{sen}\\hspace{2pt}}\n',
    '\\providecommand{\\arcsin}{} \\renewcommand{\\arcsin}{\\hspace{2pt}\\mathrm{arcsen}\\hspace{2pt}}\n',
    '\\providecommand{\\tan}{} \\renewcommand{\\tan}{\\hspace{2pt}\\mathrm{tg}\\hspace{2pt}}\n',
    '\\providecommand{\\cot}{} \\renewcommand{\\cot}{\\hspace{2pt}\\mathrm{cotg}\\hspace{2pt}}\n',
    '\\providecommand{\\csc}{} \\renewcommand{\\csc}{\\hspace{2pt}\\mathrm{cosec}\\hspace{2pt}}\n',
    '\\newcommand{\\B}{\\item[$\\bullet$]}\n',
    '\\newcommand{\\tab}{\\phantom{xxxx}}\n',
    '\\usepackage{booktabs}\n',
    '\\usepackage{lscape}\n',
    '\\begin{document}\n',
    '\\begin{center}\n',
    '\\textbf{Title}\\\\\n',
    'Subtitle \\\\\\vspace{36pt}\n',
    '\\end{center}\n',
    '\\end{document}\n'
]

class PathPattern(Enum):
    LINUX = 0 
    WINDOWS = 1

class Action(Enum):
    MOVE = 0
    COPY = 1

class Latex:
    
    def __init__(self, latex_file, path_pattern=PathPattern.LINUX):
        self.latex_file = latex_file

        if path_pattern == PathPattern.LINUX:
            self.separator = '/'
        else:
            self.separator = '\\'

        self.root_dir, self.pictures_folder = self.__create_folders()
        if not isfile(latex_file):
            self.create_new_file()


    # creates picture and root folder
    def __create_folders(self):
        if 

        i = self.latex_file.rfind(self.separator)
        if i == -1:
            root_dir = '.' + self.separator
        else:
            root_dir = self.latex_file[:i+1]
        
        pictures_folder = self.root_dir + 'pictures' + self.separator
        if not isdir(pictures_folder):
            os.mkdirs(pictures_folder)
        
        return root_dir, pictures_folder

    # throws IOError when override is False and the file exists
    def create_new_file(self, override=False):
        self.root_dir, self.pictures_folder = self.__create_folders()
        if isfile(self.latex_file):
            if override:
                os.remove(self.create_new_file)
            else:
                raise IOError('File ' + self.latex_file + ' already ' + \
                    'exists!')

        with codecs.open(self.latex_file, 'w', encoding='utf8') as newfile:
            newfile.writelines(abnt_default)

    # Insert code in the latex_file. line_to_insert=0 will insert at the end
    def insert_in_file(self, latex_code, line_to_insert=0):
        current_line = 1
        with codecs.open(self.latex_file, 'r', encoding='utf8', 
                errors='ignore') as ltx:
            with codecs.open('tmp.tex', 'w', encoding='utf8', 
                    errors='ignore') as tmp:
                for ltx_line in ltx: 
                    # escreve no final
                    if line_to_insert == 0 \
                        and ltx_line.startswith('\end{document}'): 
                        self.__write_latex_code(latex_code, tmp)
                    elif line_to_insert == current_line:
                        self.__write_latex_code(latex_code, tmp)
                    tmp.writelines(ltx_line)
                    current_line += 1
        os.remove(self.latex_file)
        os.rename('tmp.tex', self.latex_file)
        
 
    # support fir insert_in_file, it places latex_code in the specific line
    # position 
    def __write_latex_code(self, latex_code, tmp):
        if type(latex_code) == 'str':
            tmp.write(latex_code + '\n')
        else:    
            for newline in latex_code:
                tmp.writelines(newline)

    # insert code for image in latex_file
    def insert_image(self, image_file, line_to_insert=0, scale=0.5):
        self.insert_in_file('\insertgraphics[scale=' + str(scale) + ']{' + 
                image_file + '}')
    
    # move or copy the image to the project's picture folder
    def move_image(self, image_file, action=Action.MOVE):
        
    
        if action == Action.MOVE:
            os.rename(image_file, self.pictures_folder + )

    def move_insert_image(self, image_file, line_to_insert=0, scale=0.5):
        self.move_image(image_file)

    def __parse_image_file(self, image_file):
        
