from pathlib import Path

from .dosierojn_ls import CelDosiero, FontDosiero
from .lingvaj_konstantoj import LEKSEMARO, MORFEMARO
from .utils import senfinajxigi


def radikigi(vortara_vorto):
    return senfinajxigi(
        vortara_vorto,
        finajxoj=MORFEMARO.vortaraj_finajxoj,
        esceptoj=MORFEMARO.afiksoj + LEKSEMARO.cxiuj_vortetoj,
    )


class Vortaro:
    def __init__(self, kore={}):
        self.kore = kore
        # выводится в качестве значения слова, если значение слова не определено
        self.nomo_por_None = "@ не определено"
        self.sep = "\t"

    def elsxuti_el_dosieron(self, dvojo):
        """Считать словарь из файла"""
        linioj = FontDosiero(dvojo).legi_liniojn()
        for row in linioj:
            kamp_num = 3
            split = row.strip().split(self.sep, maxsplit=kamp_num-1)
            key = split[0].lower()
            if key.isspace():
                continue
            split = split + ["" for i in range(kamp_num - len(split))]
            value = split[1]
            comment = split[2]
            self.kore[key] = f"{value}{self.sep}{comment}"
        return self

    def subvortaro(self, vortoj):
        """Вернуть подсловарь со словами из vortoj"""
        new_kore = {}
        for key in vortoj:
            key = key.lower()
            new_kore[key] = self.kore.get(key, None)
        return Vortaro(new_kore)

    def cxefvortoj_el_radiko(self):
        """Словарь: radiko -> [cxefvorto_1, cxefvorto_2, ]"""
        radikoj = self.radikoj(output_format="list")
        rezulto = {radiko: [] for radiko in radikoj}
        for cxefvorto in self.kore.keys():
            radiko = radikigi(cxefvorto)
            rezulto[radiko].append(cxefvorto)
        return rezulto

    def radikoj(self, output_format="list"):
        if output_format == "set":
            return set(map(lambda x: radikigi(x), self.kore.keys()))
        elif output_format == "list":
            return list(map(lambda x: radikigi(x), self.kore.keys()))
        elif output_format == "dict":
            return dict(
                map(lambda x: (x, radikigi(x)), self.kore.keys())
            )  # Словарь: cxefvorto -> radiko
        else:
            return map(lambda x: radikigi(x), self.kore.keys())

    def html(self):
        """Вернуть словарь в виде текста в формате html"""
        output = ""
        cxelo = '<td style="vertical-align:top;">{}</td>'
        sxablono = f"<tr>{cxelo}{cxelo}{cxelo}</tr>\n"
        for key, value in self.kore.items():
            key = f"<b>{key}</b>"
            if value is not None:
                lkrampo = value.count("(")
                rkrampo = value.count(")")
                if lkrampo == rkrampo:
                    value = value.replace("(", "<i>(").replace(")", "</i>)")
            else:
                value = self.nomo_por_None
            split = value.split(self.sep)
            value = split[0]
            comment = split[1] if len(split) > 1 else ""
            output += sxablono.format(key, value, comment)
        output = f"<table>\n{output}</table>"
        return output

    def txt(self):
        """Вернуть словарь в виде текста формате txt"""
        output = ""
        for key, value in self.kore.items():
            value = value if value is not None else self.nomo_por_None
            output += sxablono.format(key, value)
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
        output = switch[dvojo.suffix]()
        CelDosiero(dvojo).skribi(output)


# Загрузить словарь из файла
BAZA_VORTARO = Vortaro().elsxuti_el_dosieron(
    Path(__file__).parent / ".." / "data" / "bazavortaro.txt"
)
