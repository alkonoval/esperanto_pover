import os

# Сохранить vortetoj в словарь
from modules.lingvaj_konstantoj import MORFEMARO, LEKSEMARO
from modules.dosierojn_ls import CelDosiero
CelDosiero('cxiuj_vortetoj.txt').skribi_vortliston(LEKSEMARO.cxiuj_vortetoj)

## Сохранить весь базовый словарь в html.формате
#from modules.vortaro import BAZA_VORTARO
#BAZA_VORTARO.save('Baza_vortaro')

# Протестировать разбор слова
#from modules.disigi import Gramatiko, Dismorfemo
#from modules.dosierojn_ls import x_igi
#vorto = x_igi('dio-sekunda')
#vdis = Dismorfemo(vorto)
#for k, it in vdis.__dict__.items():
    #print(k, it)
#print(vdis)

## Протестировать разбитие на слова
#from modules.teksto import Teksto
##teksto = Teksto().elsxuti_el_dosieron(dnomo = 'Teksto.txt')
#teksto = Teksto('20a 123')
#teksto.prilabori()
#print(teksto.spliti_al_vortoj(ignori_nombrojn = False))
