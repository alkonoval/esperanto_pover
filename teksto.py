import re

from dosierojn_ls import FontDosiero, CelDosiero, x_igi, DATA_DIR
from konstantaro import MORFEMARO, LEKSEMARO
from utils import forigi_ripetojn_konservante_ordon
from disigi import Dismorfemo

from vortaro import BAZA_VORTARO, Vortaro

class Teksto:
    
    def __init__(self, teksto=''):
        self.teksto = teksto
    
    def elsxuti_el_dosieron(self, dnomo):
        self.teksto = FontDosiero(dnomo).legi()
        return self
    
    def spliti_al_vortoj(self, cel_dnomo = None):
        """Выдать слова, встерчающиеся в тексте и записать из в файл cel_dnomo (если требуется)"""
        vortoj = re.findall("[a-z']+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = forigi_ripetojn_konservante_ordon(vortoj)
        if cel_dnomo is not None:
            CelDosiero(cel_dnomo, formatilo = x_igi).skribi_vortliston(rezulto)
        return rezulto
    
    def spliti_al_fragmentoj(self):
        pass
    
    def vortareto(self, vortaro = BAZA_VORTARO):
        vortoj = self.spliti_al_vortoj()
        radikoj = []
        nekonataj_vortoj = []
        for vorto in vortoj:
            vdis = Dismorfemo(vorto)
            vortradikoj = vdis.radikoj
            radikoj += vortradikoj
            if vdis.disigoj == []:
                nekonataj_vortoj.append(vorto)
        cxefvortoj_el = vortaro.cxefvortoj_el_radiko()
        vortaraj_vortoj = []
        for radiko in radikoj:
            vortaraj_vortoj += cxefvortoj_el[radiko]
        return vortaro.subvortaro(vortaraj_vortoj + nekonataj_vortoj)
    
    def dismorfigi(self, cel_dnomo = None):
        vortoj = self.spliti_al_vortoj()
        rezulto = {} # слово -> его разбор
        for vorto in vortoj:
            vdis = Dismorfemo(vorto)
            if vdis.disigoj != []:
                rezulto[vorto] = str(vdis)
                #rezulto[vorto] = str(vdis.radikoj)
                #rezulto[vorto] = str(vdis.disigoj)
            else:
                rezulto[vorto] = 'Не удалось разобрать'
        if cel_dnomo is not None:
            #CelDosiero(cel_dnomo).skribi_dict(rezulto)
            Vortaro(rezulto).save(dnomo = cel_dnomo)
        return rezulto

if __name__ == '__main__':
    # Разбить текст на слова
    teksto = Teksto().elsxuti_el_dosieron(dnomo = 'Teksto_1_SL.txt')
    #teksto.spliti_al_vortoj(cel_dnomo = '2_SL.txt')
    
    # Произвести морфологический разбор всех слов текста
    teksto.dismorfigi(cel_dnomo = 'Dismorfemo')
    
    # Получить словарик для слов из текста
    teksto.vortareto().save(dnomo = 'Vortareto')
    
    
