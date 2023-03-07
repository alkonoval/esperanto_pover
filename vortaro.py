from dosierojn_ls import FontDosiero, CelDosiero, DATA_DIR
from konstantaro import MORFEMARO, LEKSEMARO
from konstantaro import senfinajxigi

def radikigi(vortara_vorto):
    return senfinajxigi(vortara_vorto, finajxoj = MORFEMARO.vortaraj_finajxoj, esceptoj = LEKSEMARO.cxiuj_vortetoj)

class Vortaro:
    def __init__(self, kore = {}):
        self.kore = kore
        self.nomo_por_None = "@ не определено" # выводится в качестве значения слова, если значение слова не определено
        
    def elsxuti_el_dosieron(self, dnomo):
        """Считать словарь из файла"""
        linioj = FontDosiero(dnomo, dirnomo = DATA_DIR).legi_liniojn()
        for row in linioj:
            kamp_num = 3
            #split = eniga_formatilo(row.strip()).split('\t', maxsplit=2)
            split = row.strip().split('\t', maxsplit=2)
            key = split[0].lower()
            if key.isspace():
                continue
            split = split + ['' for i in range(kamp_num - len(split))]
            value = split[1]
            comment = split[2]
            self.kore[key] = f"{value}\t{comment}"
        return self
        
    def subvortaro(self, vortoj):
        """Вернуть подсловарь со словами из vortoj"""
        new_kore = {}
        for key in vortoj:
            key = key.lower()
            new_kore[key] = self.kore.get(key, None)
        return Vortaro(new_kore)
    
    def cxefvorto_al_radiko(self):
        new_kore = dict(map(lambda x: (x, radikigi(x)), self.kore.keys()))
        return Vortaro(new_kore)
    
    def radiko_al_cxefvorto(self):
        it = map(lambda x: (radikigi(x), x), self.kore.keys())
        return Vortaro(dict(it)) # !!! Потеря некоторых слов w для которых radikigi(w) не уникально
    
    def radikoj(self):
        #return set(map(lambda x: radikigi(x), self.kore.keys()))
        return list(map(lambda x: radikigi(x), self.kore.keys()))
    
    def html(self):
        """Вернуть словарь в виде текста в формате html"""
        output = ''
        cxelo = '<td style="vertical-align:top;">{}</td>'
        sxablono = f'<tr>{cxelo}{cxelo}{cxelo}</tr>\n'
        #sxablono = f'<tr>{cxelo}{cxelo}</tr>\n'
        for key, value in self.kore.items():
            key = f'<b>{key}</b>'
            if value is not None:
                lkrampo = value.count('(')
                rkrampo = value.count(')')
                if lkrampo == rkrampo:
                    value = value.replace('(', '<i>(').replace(')', '</i>)')
            else:
                value = self.nomo_por_None
            split = value.split('\t')
            value = split[0]
            comment = split[1] if len(split) > 1 else ''
            output += sxablono.format(key, value, comment)
            #output += sxablono.format(key, value)
        output = f'<table>\n{output}</table>'
        return output
    
    def txt(self):
        """Вернуть словарь в виде текста формате txt"""
        output = ''
        sxablono = '{}\t{}\n'
        for key, value in self.kore.items():
            value = value if value is not None else self.nomo_por_None
            output += sxablono.format(key, value)
        return output
    
    def save(self, dnomo, dosiertipo = 'html'):
        """Записать словарь файл в одном из форматов: txt, html"""
        switch = {'html' : self.html, 'txt': self.txt}
        if dosiertipo not in switch:
            print('Eraro: Maltauxga dosiertipo:', dosiertipo)
            print('Tauxgaj dosiertipoj:', ', '.join(switch.keys()))
            return
        dnomo = f"{dnomo}.{dosiertipo}"
        output = switch[dosiertipo]()
        CelDosiero(dnomo).skribi(output)

if __name__ == '__main__':
    # Загрузить словарь из файла
    vortaro = Vortaro()
    vortaro.elsxuti_el_dosieron('bazavortaro.txt')
    
    # Сохранить весь словарь в формате html
    #vortaro.save(dnomo = "tuta_bazvortaro", dosiertipo = 'html')
    
    # Подсловарь для слов из файла
    vortoj = FontDosiero('P_1.txt').legi_vortliston()
    subvortaro = vortaro.subvortaro(vortoj)
    subvortaro.save(dnomo = 'P_2', dosiertipo = 'html')
    
    # Словарь: слово -> основа (слово без окончания)
    radikigo = vortaro.cxefvorto_al_radiko()
    radikigo.save(dnomo = 'Radikigo', dosiertipo = 'html')
    
