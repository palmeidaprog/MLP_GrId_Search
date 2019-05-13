import codecs
import os
from os.path import isfile, isdir
from os import makedirs
from enum import Enum
from shutil import copy2

abnt_default = [
    '\\documentclass[12pt,a4paper]{article}\n',
    '\\usepackage[T1]{fontenc}\n',
    '\\usepackage{graphicx}\n',
    '\\usepackage{times}\n',
    '\\graphicspath{ {pictures/} }\n',
    '%\\usepackage{xcolor}\n',
    '\\usepackage[formats]{listings}\n',
    '\\setlength{\\parindent}{0pt}\n',
    '\\usepackage[utf8]{inputenc}\n',
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
    # Creates a latex_file and the project's folder coupled with a 
    # subfolder named pictures. 
    # 
    # In case you are using windowns path separator \\ change path_pattern
    # to PathPattern.WINDOWS, to parse the path correctly 
    # 
    # If the latex_file doesn't exist it will be created based on abnt_default
    # you can set any template for the new file on a iterable structure like 
    # list
    # 
    def __init__(self, latex_file, path_pattern=PathPattern.LINUX, 
            template=abnt_default):
        self.latex_file = latex_file
        self.template = template

        if path_pattern == PathPattern.LINUX:
            self.separator = '/'
        else:
            self.separator = '\\'

        self.root_dir, self.pictures_folder = self.__create_folders()
        if not isfile(latex_file):
            self.create_new_file()

    # creates picture and root folder
    def __create_folders(self):
        i = self.latex_file.rfind(self.separator)
        root_dir = ''
        if i == -1:
            root_dir = '.' + self.separator
        else:
            root_dir = self.latex_file[:i+1]
        
        pictures_folder = root_dir + 'pictures' + self.separator
        if not isdir(pictures_folder):
            makedirs(pictures_folder)
        
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

    # add latex code to centralize the output
    def __centralize(self, latex_code):
        return '\\begin{center}\n' + latex_code + '\\end{center}\n'

    # adds a new line in latex code '\\' 
    def __add_linefeed(self, latex_code):
        return latex_code + '\\\\\n'

    # Insert code in the latex_file. line_to_insert=0 will insert at the end
    # linefeed as True adds a latex's end of the line (\\)
    # centerd = True if you need the text to be centered in the PDF file
    def insert_in_file(self, latex_code, line_to_insert=0, linefeed=False,
            centered=False):
        current_line = 1

        with codecs.open(self.latex_file, 'r', encoding='utf8', 
                errors='ignore') as ltx:
            with codecs.open('tmp.tex', 'w', encoding='utf8', 
                    errors='ignore') as tmp:
                for ltx_line in ltx: 
                    # escreve no final
                    if line_to_insert == 0 \
                        and ltx_line.startswith('\\end{document}'): 
                        self.__write_latex_code(latex_code, tmp, linefeed, 
                            centered)
                    elif line_to_insert == current_line:
                        self.__write_latex_code(latex_code, tmp, linefeed,
                            centered)
                    tmp.writelines(ltx_line)
                    current_line += 1
        #copy2(self.latex_file, 'xx.tex')
        os.remove(self.latex_file)
        os.rename('tmp.tex', self.latex_file)

    def __format_code(self, latex_code, linefeed=False, centered=False):
        if linefeed:
            latex_code = self.__add_linefeed(latex_code) 
        if centered:
            latex_code = self.__centralize(latex_code)
        return latex_code
        
    # support fir insert_in_file, it places latex_code in the specific line
    # position 
    def __write_latex_code(self, latex_code, tmp, linefeed, centered):
        if type(latex_code) == str:
            latex_code = self.__format_code(latex_code, linefeed, centered)
            tmp.write(latex_code)
        else:    
            for newline in latex_code:
                newline = self.__format_code(newline, linefeed, centered)
                tmp.writelines(newline)

    # insert code for image in latex_file
    def insert_image(self, image_file, line_to_insert=0, scale=0.5, 
            linefeed=True):
        self.insert_in_file('\\insertgraphics[scale=' + str(scale) + ']{' + 
                image_file + '}\n', linefeed=linefeed, centered=True)

    # move or copy the image to the project's picture folder
    # action = Move picture to the latex picture
    def move_image(self, image_file, action=Action.MOVE, 
            auto_rename_file=True):
        # rename picture in case it exists in the destination

        print(self.__parse_filename(image_file))
        if action == Action.MOVE:
            print(self.__parse_filename(image_file))
            os.rename(image_file, self.pictures_folder + 
                    self.__parse_filename(image_file))
        elif action == Action.COPY:
            copy2(image_file, self.pictures_folder + \
                    self.__parse_filename(image_file))

    def move_insert_image(self, image_file, line_to_insert=0, scale=0.5):
        self.move_image(image_file)
        self.insert_image(image_file)

    #return the parent folder
    def __parse_parent_dir(self, file):
        i = file.rfind(self.separator)
        if i == -1:
            base_dir = '.' + self.separator
        else:
            base_dir = file[:i+1]
        return base_dir

    # return only the file of a pathname 
    def __parse_filename(self, file):
        i = file.rfind(self.separator)
        if i != -1:
            file = file[i+1:]
            
        return file