## Протестировать разбор слова
from modules.dismorfemigilo import Dismorfemo
from modules.dosierojn_ls import x_igi

# Теситровать vortetoj
# from modules.lingvaj_konstantoj import MORFEMARO, LEKSEMARO, VORTETOJ, rafini_vorteton
# from modules.dismorfemigilo import *
# from modules.dosierojn_ls import CelDosiero
# cxiuj_vortetoj = LEKSEMARO.cxiuj_vortetoj
# print(rafini_vorteton('kien'))
# CelDosiero('cxiuj_vortetoj.txt').skribi_vortliston(cxiuj_vortetoj)
# CelDosiero('cxiuj_vortetoj.txt').skribi_dict(vorteto_al_speco)


## Сохранить весь базовый словарь в html.формате
# from modules.vortaro import BAZA_VORTARO
# BAZA_VORTARO.save('Baza_vortaro')


vorto = x_igi("kvankam")
vdis = Dismorfemo(vorto)
for k, it in vdis.__dict__.items():
    print(k, it)
print(vdis)

## Протестировать разбитие на слова
# from modules.teksto import Teksto
##teksto = Teksto().elsxuti_el_dosieron(dnomo = 'Teksto.txt')
# teksto = Teksto('20a 123')
# teksto.prilabori()
# print(teksto.spliti_al_vortoj(ignori_nombrojn = False))

## Удаление элементов из списка
# from modules.utils import listo_sen_certaj_elementoj
# listo1 = [1, 2, 3, 3, 1, 2]
# listo2 = [3, 4, 1]
# print(listo1, listo2, listo_sen_certaj_elementoj(listo1, listo2), sep = '\n')
