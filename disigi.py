import re

from dosierojn_ls import FontDosiero, CelDosiero, x_igi, DATA_DIR
from konstantaro import MORFEMARO, LEKSEMARO, senfinajxigi
from vortaro import Vortaro

class Teksto:
    
    def __init__(self, teksto=''):
        self.teksto = teksto
    
    def elsxuti_el_dosieron(self, dnomo):
        self.teksto = FontDosiero(dnomo).legi()
        return self
    
    def spliti_al_vortoj(self, cel_dnomo = None):
        """Выдать слова, встерчающиеся в тексте и записать из в файл cel_dnomo (если требуется)"""
        vortoj = re.findall("[a-z']+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = []
        for vorto in vortoj:
            if vorto not in rezulto:
                rezulto.append(vorto)
        if cel_dnomo is not None:
            CelDosiero(cel_dnomo, formatilo = x_igi).skribi_vortliston(rezulto)
        return rezulto
    
    def disigi(self, radikaro, cel_dnomo = None):
        vortoj = self.spliti_al_vortoj()
        radikaro = set(radikaro)
        rezulto = {} # слово -> его разбор
        for vorto in vortoj:
            disv = Dismorfemo(vorto, radikoj = radikaro)
            rezulto[vorto] = disv.ricevi()
        if cel_dnomo is not None:
            CelDosiero(cel_dnomo).skribi_dict(rezulto)
        return rezulto

BASE = {'V': LEKSEMARO.cxiuj_vortetoj,
        'F': MORFEMARO.finajxoj,
        'A': MORFEMARO.afiksoj,
        'G': ['o', 'a'],
        'R': ['man', 'person', 'son', 'hom', 'virt']}

REGULOJ = {'w': ['V', 'bF'], 'b': ['V', 'R', 'A', 'bR', 'bA']}

def dividi(peco, regulo):
    tipo = regulo[-1]
    new_state = regulo[0] if len(regulo) > 1 else ''
    variantoj = []
    if new_state is not '':
        for mor in BASE[tipo]:
            sxablono = f'{mor}$'
            match = re.search(sxablono, peco)
            if match:
                left_peco = re.split(sxablono, peco)[0]
                if left_peco is not '':
                    rez = [(left_peco, new_state), (mor, tipo)]
                    variantoj.append(rez)
    else:
        for mor in BASE[tipo]:
            if peco == mor:
                rez = (('', new_state), (mor, tipo))
                variantoj.append(rez)
    return variantoj

def dismorfemi(peco, state = 'w'):
    variantoj = []
    for regulo in REGULOJ[state]:
        rez = dividi(peco, regulo)
        variantoj += rez
    rezulto = []
    for vr in variantoj:
        new_peco = vr[0][0]
        new_state = vr[0][1]
        mor_kun_tipo = vr[1]
        if new_peco is '':
            rez = [mor_kun_tipo]
            rezulto.append(rez)
        else:
            rekuro = dismorfemi(new_peco, new_state)
            if rekuro is []:
                continue
            rez = []
            for it in rekuro:
                rez.append(it + [mor_kun_tipo])
            rezulto += rez
    return rezulto
            
class Dismorfemo:
    def __init__(self, vorto, radikoj):
        self.radikoj = set(radikoj)
        self.vorto = vorto.lower()
        self.radikalo = self.ricevi_radikalon()
    
    def ricevi(self):
        self.malmultigi_eblajn_radikojn()
        BASE['R'] = self.radikoj
        rez = dismorfemi(self.vorto)
        rezs = []
        for r in rez:
            out = '-'.join(map(lambda x: x[0], r))
            rezs.append(out)
        return ', '.join(rezs)
                        
    def ricevi_radikalon(self):
        rezulto = senfinajxigi(self.vorto, finajxoj = MORFEMARO.finajxoj, esceptoj = LEKSEMARO.cxiuj_vortetoj)
        return rezulto
    
    def malmultigi_eblajn_radikojn(self):
        rezulto = []
        vorto = self.radikalo
        esceptoj = set(LEKSEMARO.cxiuj_vortetoj + MORFEMARO.afiksoj)
        subvortoj = [vorto[i:j] for i in range(len(vorto)) for j in range(i + 1, len(vorto) + 1)]
        for radiko in subvortoj:
            if radiko in esceptoj:
                continue
            if radiko in self.radikoj:
                rezulto.append(radiko)
        self.radikoj = rezulto

if __name__ == '__main__':
    # Разбить текст на слова
    teksto = Teksto().elsxuti_el_dosieron(dnomo = '1_SL.txt')
    #teksto.spliti_al_vortoj(cel_dnomo = '2_SL.txt')
    
    # Произвести морфологический разбор
    vortaro = Vortaro().elsxuti_el_dosieron('bazavortaro.txt')
    teksto.disigi(radikaro = vortaro.radikoj(), cel_dnomo = 'Dismorfemo.txt')
    
    #BASE['R'] = ['man', 'person', 'son', 'hom', 'virt']
    #rez1 = dismorfemi('persone', state = 'w')
    #rez2 = dismorfemi('malvirtulo', state = 'w')
    
