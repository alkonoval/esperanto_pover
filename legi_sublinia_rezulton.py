import re

from dosierojn_ls import FontDosiero, CelDosiero
from vortaro import Vortaro
from utils import forigi_ripetojn_konservante_ordon

def ricevi_cxefvortojn(dnomo):
    """Прочитать результат программы Sublinio и выделить найденные слова/корни"""
    linioj = FontDosiero(dnomo).legi_liniojn()
    linioj = [linioj[x].strip() for x in range(1, len(linioj), 2)] # выделить четные строки
    cexvortoj = []
    #nekonatoj = []
    for linio in linioj:
        if linio.find('[') == -1:
            #nekonatoj.append(linio)
            cexvortoj.append(f'{linio}#')
        else:
            cexvortoj += linio.split('[')[1].split(']')[0].split('~')
    return forigi_ripetojn_konservante_ordon(cexvortoj)#, nekonatoj

if __name__ == '__main__':
    vortaro = Vortaro()
    vortaro.elsxuti_el_dosieron('bazavortaro.txt')
    vortoj = ricevi_cxefvortojn('3_SL.txt')
    #vortaro.subvortaro(vortoj).save(dnomo = '4_SL', dosiertipo = 'html')
    CelDosiero('4_SL.txt').skribi_vortliston(vortoj)
    
    
