"""Чтение и записть файлов"""
import os

INPUT_DIR = './input'
OUTPUT_DIR = './output'
DATA_DIR = './data'
for dirname in [OUTPUT_DIR]:
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    if not os.path.isdir(dirname):
        pass
#def ekscii_dir(path):
    #return os.path.dirname(os.path.abspath(path))
    

diakritajxoj = ["ĉ", "ĝ", "ĥ", "ĵ", "ŝ", "ŭ"]
Diakritajxoj = ["Ĉ", "Ĝ", "Ĥ", "Ĵ", "Ŝ", "Ŭ"]
def x_igi(teksto):
    rez = teksto
    rez = rez.replace('ĉ', 'cx').replace('ĝ', 'gx').replace('ĥ', 'hx').replace('ĵ', 'jx').replace('ŝ', 'sx').replace('ŭ', 'ux')
    rez = rez.replace('Ĉ', 'Cx').replace('Ĝ', 'Gx').replace('Ĥ', 'Hx').replace('Ĵ', 'Jx').replace('Ŝ', 'Sx').replace('Ŭ', 'Ux')
    return rez
def sen_x_igi(teksto):
    rez = teksto
    rez = rez.replace('cx', 'ĉ').replace('gx', 'ĝ').replace('hx', 'ĥ').replace('jx', 'ĵ').replace('sx', 'ŝ').replace('ux', 'ŭ')
    rez = rez.replace('Cx', 'Ĉ').replace('Gx', 'Ĝ').replace('Hx', 'Ĥ').replace('Jx', 'Ĵ').replace('Sx', 'Ŝ').replace('Ux', 'Ŭ')
    rez = rez.replace('CX', 'Ĉ').replace('GX', 'Ĝ').replace('HX', 'Ĥ').replace('JX', 'Ĵ').replace('SX', 'Ŝ').replace('UX', 'Ŭ')
    return rez

class FontDosiero():
    """Файл для чтения"""
    
    def __init__(self, dnomo, encoding ='utf-8-sig', dirnomo = INPUT_DIR, formatilo = x_igi):
        self.dnomo = dnomo
        self.encoding = encoding
        self.formatilo = formatilo
        self.dirnomo = dirnomo
        
    def legi(self):
        """Прочитать файл, результат чтения выдать как одну большую строку"""
        dosiero = open(os.path.join(self.dirnomo, self.dnomo), 'r', encoding=self.encoding)
        rezulto = self.formatilo(dosiero.read())
        dosiero.close()
        return rezulto
    
    def legi_liniojn(self):
        """Прочитать файл, результат чтения выдать как одну большую строку"""
        dosiero = open(os.path.join(self.dirnomo, self.dnomo), 'r', encoding=self.encoding)
        rezulto = [self.formatilo(linio) for linio in dosiero.readlines()]
        dosiero.close()
        return rezulto
    
    def legi_vortliston(self):
        """Считать список слов из файла. Предополается, что в файле каждое слово расположено на отдельной строке."""
        linioj = self.legi_liniojn()
        vortoj = []
        for linio in linioj:
            vorto = linio.strip()
            if vorto not in vortoj:
                vortoj.append(vorto)
        return vortoj

class CelDosiero():
    """Файл для записи"""
    
    def __init__(self, dnomo, encoding ='utf-8', dirnomo = OUTPUT_DIR, formatilo = sen_x_igi):
        self.dnomo = dnomo
        self.encoding = encoding
        self.formatilo = formatilo
        self.dirnomo = dirnomo
    
    def skribi(self, teksto):
        path = os.path.abspath(os.path.join(self.dirnomo, self.dnomo))
        dosiero = open(path, 'w', encoding=self.encoding)
        dosiero.write(self.formatilo(teksto))
        dosiero.close()
    
    def skribi_liniojn(self, linioj):
        output = '\n'.join(linioj)
        self.skribi(output)
        
    def skribi_vortliston(self, vortoj):
        self.skribi_liniojn(vortoj)
    
    def skribi_dict(self, dic, sep = '\t'):
        self.skribi_liniojn([f'{key}{sep}{val}' for key, val in dic.items()])

