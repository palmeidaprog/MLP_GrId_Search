import codecs
import os

class InsertLatex:
    def __init__(self, arquivo_latex):
        self.arquivo_latex = arquivo_latex

    # 0 insire no final
    def insere_no_arquivo(self, objeto_codigo_latex, linha=0):
        lida = 1
        with codecs.open(self.arquivo_latex, 'r', encoding='utf8', 
                errors='ignore') as ltx:
            with codecs.open('tmp.tex', 'w', encoding='utf8', 
                    errors='ignore') as tmp:
                for line in ltx: 
                    if linha == 0 and line.startswith('\end{document}'): # escreve no final
                        print('colocou no final')
                        self.__escreve_latex(objeto_codigo_latex, tmp)
                    elif linha == lida:
                        self.__escreve_latex(objeto_codigo_latex, tmp)
                    tmp.writelines(line)
                    lida += 1
        os.remove(self.arquivo_latex)
        os.rename('tmp.tex', self.arquivo_latex)
        

    def __escreve_latex(self, objeto_codigo_latex, tmp):
        if type(objeto_codigo_latex) == 'str':
            tmp.write(objeto_codigo_latex + '\n')
        else:    
            for newline in objeto_codigo_latex:
                tmp.writelines(newline)

    def insere_imagem(self, nome_da_image, linha=0):
        self.insere_no_arquivo('\insertgraphics[scale=0.5]\{' + 
                nome_da_image + '\}')
        
