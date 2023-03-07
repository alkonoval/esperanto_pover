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
    
    def prilabori(self):
        self.vortoj = self.spliti_al_vortoj()
        self.dismorfigo = self.dismorfigi() # словарь: слово -> список его разборов
        #self.signo_por_nerekonita_vorto = '#'
        self.nerekonitaj_vortoj = [vorto for vorto in self.dismorfigo.keys() if self.dismorfigo[vorto].disigoj == []]
        self.vortaraj_vortoj = self.ricevi_vortarajn_vortojn()
        self.vortareto = BAZA_VORTARO.subvortaro(self.vortaraj_vortoj + self.nerekonitaj_vortoj)
    
    def spliti_al_vortoj(self, cel_dnomo = None):
        """Выдать слова, встерчающиеся в тексте и записать из в файл cel_dnomo (если требуется)"""
        vortoj = re.findall("[a-z']+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = forigi_ripetojn_konservante_ordon(vortoj)
        if cel_dnomo is not None:
            CelDosiero(cel_dnomo, formatilo = x_igi).skribi_vortliston(rezulto)
        return rezulto
    
    def ricevi_vortarajn_vortojn(self):
        radikoj = []
        for vorto in self.vortoj:
            vortradikoj = self.dismorfigo[vorto].radikoj
            radikoj += vortradikoj
        cxefvortoj_el = BAZA_VORTARO.cxefvortoj_el_radiko()
        vortaraj_vortoj = []
        for radiko in radikoj:
            vortaraj_vortoj += cxefvortoj_el[radiko]
        return vortaraj_vortoj
        
    def dismorfigi(self):
        rezulto = {} # словарь: слово -> список его разборов
        for vorto in self.vortoj:
            rezulto[vorto] = Dismorfemo(vorto)
        return rezulto
    
    def skribi_dismorfigon(self, cel_dnomo):
        kore_por_vortaro = {vorto : str(vdis) for vorto, vdis in self.dismorfigo.items()}
        #kore_por_vortaro = {vorto : str(vdis.disigoj) for vorto, vdis in self.dismorfigo.items()}
        Vortaro(kore_por_vortaro).save(dnomo = cel_dnomo)
        

if __name__ == '__main__':
    teksto = Teksto().elsxuti_el_dosieron(dnomo = 'Teksto_1_SL.txt')
    teksto.prilabori()

    # Сохранить морфологический разбор всех слов текста
    teksto.skribi_dismorfigon(cel_dnomo = 'Dismorfemo')
    
    # Получить словарик для слов из текста
    teksto.vortareto.save(dnomo = 'Vortareto')
    
    # Сохранить словарные слова
    CelDosiero('Vortaraj_vortoj_4_SL.txt').skribi_vortliston(teksto.vortaraj_vortoj + [f'{vorto}#' for vorto in teksto.nerekonitaj_vortoj])
    
    
