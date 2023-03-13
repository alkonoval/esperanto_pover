import os

# Сохранить vortetoj в словарь
from modules.lingvaj_konstantoj import MORFEMARO, LEKSEMARO, VORTETOJ
from modules.disigi import *
from modules.dosierojn_ls import CelDosiero
cxiuj_vortetoj = LEKSEMARO.cxiuj_vortetoj
vorteto_al_speco = VORTETOJ.speco
#CelDosiero('cxiuj_vortetoj.txt').skribi_vortliston(cxiuj_vortetoj)
CelDosiero('cxiuj_vortetoj.txt').skribi_dict(vorteto_al_speco)


## Сохранить весь базовый словарь в html.формате
#from modules.vortaro import BAZA_VORTARO
#BAZA_VORTARO.save('Baza_vortaro')

## Протестировать разбор слова
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

## Удаление элементов из списка
#from modules.utils import listo_sen_certaj_elementoj
#listo = [1, 2, 3]
#print(listo_sen_certaj_elementoj(listo, [2, 3]), listo)
