import re

from .dismorfemigilo import Dismorfemo
from .dosierojn_ls import CelDosiero, FontDosiero, x_igi
from .lingvaj_konstantoj import rafini_vorton
from .utils import forigi_ripetojn_konservante_ordon
from .vortaro import vortaro, Vortaro


class Teksto:
    """Класс для обработки текста"""

    def __init__(self, teksto=""):
        self.teksto = x_igi(teksto)

    def elsxuti_el_dosieron(self, dvojo):
        self.teksto = FontDosiero(dvojo).legi()
        return self

    def prilabori(self):
        # список всех слов (без повторений), встречающихся в тексте 
        self.vortoj = self.__spliti_al_vortoj() 
        # dict: слово из текста -> класс с морфологическими разборами для него
        self.dismorfigo_por = self.__dismorfigi()
        # dict: слово из текста -> список слов из словаря, которые встречаются в этом слове в качестве корня
        self.vortaraj_vortoj_por = self.__ricevi_vortarajn_vortojn_por()
        # список слов из текста, для которых морфологический разбор не дал результатов
        self.nerekonitaj_vortoj = self.__ricevi_nerekonitajn_vortojn()
        # список слов из словаря, которые встречаются в тексте в качестве корней
        self.vortaraj_vortoj = self.__ricevi_vortarajn_vortojn()
        # словарик для текста
        self.vortareto = vortaro.subvortaro(
            self.nerekonitaj_vortoj + self.vortaraj_vortoj
        )

    def __spliti_al_vortoj(self, ignori_nombrojn=True):
        """Выдать слова, встречающиеся в тексте"""
        vortoj = re.findall("[a-z'\d-]+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = forigi_ripetojn_konservante_ordon(vortoj)
        if ignori_nombrojn:
            rezulto = list(filter(lambda x: not x.isdigit(), rezulto))
        return rezulto

    def __dismorfigi(self):
        """Получить словарь: слово -> класс с морфологическими разборами для него"""
        return {vorto : Dismorfemo(vorto) for vorto in self.vortoj}
    
    def __ricevi_vortarajn_vortojn_por(self):
        cxefvortoj_el = vortaro.cxefvortoj_el_radiko()
        vortaraj_vortoj_por = {}
        for vorto in self.vortoj:
            vortaraj_vortoj_por_vorto = []
            for radiko in self.dismorfigo_por[vorto].radikoj:
                vortaraj_vortoj_por_vorto += cxefvortoj_el[radiko]
            vortaraj_vortoj_por_vorto += self.dismorfigo_por[vorto].vortetoj

            vortaraj_vortoj_por[vorto] = forigi_ripetojn_konservante_ordon(
                vortaraj_vortoj_por_vorto
            )
        return vortaraj_vortoj_por

    def __ricevi_nerekonitajn_vortojn(self):
        rezulto = [
            vorto
            for vorto in self.vortoj
            if self.dismorfigo_por[vorto].disigoj == []
        ]
        return rezulto

    def __ricevi_vortarajn_vortojn(self):
        vortaraj_vortoj = []
        for vorto in self.vortoj:
            vortaraj_vortoj += self.vortaraj_vortoj_por[vorto]
        return forigi_ripetojn_konservante_ordon(vortaraj_vortoj)

    def skribi_dismorfigon(self, dvojo, plendetala=False):
        if plendetala:
            kore_por_vortaro = {
                vorto: str(vdis.senlimigaj_disigoj)
                for vorto, vdis in self.dismorfigo_por.items()
            }
        else:
            kore_por_vortaro = {
                vorto: str(vdis) for vorto, vdis in self.dismorfigo_por.items()
            }
        Vortaro(kore_por_vortaro).save(dvojo=dvojo)

    def skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(self, dvojo):
        linioj = []
        vortaraj_vortoj = []
        for vorto in self.vortoj:
            for vortara_vorto in self.vortaraj_vortoj_por[vorto]:
                if vortara_vorto in vortaraj_vortoj:
                    continue
                else:
                    linioj.append(f"{vorto}\t{vortara_vorto}")
                    vortaraj_vortoj.append(vortara_vorto)
            if vorto in self.nerekonitaj_vortoj:
                linioj.append(f"{vorto}#\t{rafini_vorton(vorto)}")
        CelDosiero(dvojo=dvojo).skribi_liniojn(linioj)
