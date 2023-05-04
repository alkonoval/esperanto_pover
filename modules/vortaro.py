from pathlib import Path

from .tformatilo import x_igi, sen_x_igi
from .lingvaj_konstantoj import LEKSEMARO, MORFEMARO
from .utils import senfinajxigi

def radikigi(vortara_vorto):
    return senfinajxigi(
        vortara_vorto,
        finajxoj=MORFEMARO.vortaraj_finajxoj,
        esceptoj=MORFEMARO.afiksoj + LEKSEMARO.cxiuj_vortetoj,
    )

class Vortaro:
    """
    Словарь: слово на эсперанто -> значение
    """
    def __init__(self, kore={}, kamp_num = 2):
        self.kore = {x_igi(key) : value for key, value in kore.items()}
        # выводится в качестве значения слова, если значение слова не определено
        self.nomo_por_None = "@ не определено"
        self.sep = "\t"
        self.kamp_num = kamp_num # число колонок словаря (включая key)
        self.prilabori()
    
    def prilabori(self):
        # Множество корней словарных слов
        self.radikoj = set(map(lambda x: radikigi(x), self.kore.keys()))
        # Словарь: radiko -> [cxefvorto_1, cxefvorto_2, ]
        cxefvortoj_el = {radiko: [] for radiko in self.radikoj}
        for cxefvorto in self.kore.keys():
            radiko = radikigi(cxefvorto)
            cxefvortoj_el[radiko].append(cxefvorto)
        self.cxefvortoj_el_radiko = cxefvortoj_el

    def elsxuti_el_dosieron(self, dvojo, kamp_num = 3):
        """Считать словарь из файла"""
        self.kamp_num = kamp_num
        linioj = Path(dvojo).read_text().splitlines()
        for row in linioj:
            # разбить строку на kamp_num полей
            split = row.strip().split(self.sep, maxsplit=self.kamp_num-1)
            key = x_igi(split[0].lower())
            if key.isspace():
                continue
            # дополнить недостающие поля до числа kamp_num
            split = split + ["" for i in range(self.kamp_num - len(split))]
            values = split[1:]
            self.kore[key] = self.sep.join(values)
        self.prilabori()
        return self

    def subvortaro(self, vortoj):
        """Вернуть подсловарь со словами из vortoj"""
        new_kore = {}
        for key in vortoj:
            key = key.lower()
            new_kore[key] = self.kore.get(key, None)
        return Vortaro(new_kore, kamp_num = self.kamp_num)

    def html(self):
        """Вернуть словарь в виде текста в формате html"""
        output = ""
        cxeloj = '<td style="vertical-align:top;">{}</td>' * self.kamp_num
        sxablono = f"<tr>{cxeloj}</tr>\n"
        for key, value in self.kore.items():
            key = f"<b>{key}</b>"
            if value is not None:
                lkrampo = value.count("(")
                rkrampo = value.count(")")
                if lkrampo == rkrampo:
                    value = value.replace("(", "<i>(").replace(")", "</i>)")
            else:
                value = self.nomo_por_None + self.sep * (self.kamp_num - 1)
            split = value.split(self.sep, maxsplit=self.kamp_num-1)
            kampoj = [key] + split
            output += sxablono.format(*kampoj)
        output = f"<table>\n{output}</table>"
        return output

    def txt(self):
        """Вернуть словарь в виде текста формате txt"""
        output = ""
        for key, value in self.kore.items():
            value = value if value is not None else self.nomo_por_None
            output += f"{key}{self.sep}{value}"
        return output

    def save(self, dvojo):
        """Записать словарь файл в одном из форматов: txt, html"""
        if dvojo.suffix == '':
            dvojo = dvojo.with_name(f"{dvojo.name}.html")
        switch = {".html": self.html, ".txt": self.txt}
        if dvojo.suffix not in switch:
            print("Eraro: Maltauxga dosiertipo:", dvojo.suffix)
            print("Tauxgaj dosiertipoj:", ", ".join(switch.keys()))
            return
        output = sen_x_igi(switch[dvojo.suffix]())
        Path(dvojo).write_text(output, encoding="utf-8")