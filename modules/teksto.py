import re
from pathlib import Path

from .dismorfemigilo import Dismorfemo, rafini_vorton
from .tformatilo import sen_x_igi
from .utils import forigi_ripetojn_konservante_ordon
from .vortaro import html

OUTPUT_DIR = Path("./output")

class Analizilo:
    """Класс для обработки текста"""

    def __init__(self, database):
        self.database = database
        self.vortaraj_radikoj = self.database.get_roots()

    def prilabori(self, teksto):
        self.teksto = teksto
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
        self.vortareto = self.database.get_litle_dictionary(
            self.nerekonitaj_vortoj + self.vortaraj_vortoj
        )

    def __spliti_al_vortoj(self, ignori_nombrojn=True):
        """Выдать слова, встречающиеся в тексте"""
        
        vortoj = re.findall("[a-zĉĝĥĵŝŭ'\d-]+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = forigi_ripetojn_konservante_ordon(vortoj)
        if ignori_nombrojn:
            rezulto = list(filter(lambda x: not x.isdigit(), rezulto))
        return rezulto

    def __dismorfigi(self):
        """Получить словарь: слово -> класс с морфологическими разборами для него"""
        return {vorto : Dismorfemo(vorto, self.vortaraj_radikoj) for vorto in self.vortoj}
    
    def __ricevi_vortarajn_vortojn_por(self):
        cxefvortoj_el = self.database.get_words_from_root
        vortaraj_vortoj_por = {}
        for vorto in self.vortoj:
            vortaraj_vortoj_por_vorto = []
            for radiko in self.dismorfigo_por[vorto].radikoj:
                vortaraj_vortoj_por_vorto += cxefvortoj_el(radiko)
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
        output = sen_x_igi('\n'.join(linioj))
        Path(dvojo).write_text(output, encoding="utf-8")

    def write_down(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Сохранить морфологический разбор всех слов текста
        output = [
            (sen_x_igi(vorto), ', '.join([str(d) for d in vdis.senlimigaj_disigoj]))
            for vorto, vdis in self.dismorfigo_por.items()
        ]
        output = html(output)
        Path(OUTPUT_DIR / "Dismorfemo.html").write_text(output, encoding="utf-8")

        # Получить словарик для слов из текста
        output = html(self.vortareto)
        Path(OUTPUT_DIR / "Vortareto.html").write_text(output, encoding="utf-8")

        # Сохранить словарные слова
        self.skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(
            OUTPUT_DIR / "Vortaraj_vortoj.txt"
        )