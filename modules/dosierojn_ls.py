"""Чтение и запись файлов"""

sendiakritigi = {
    "ĉ": "cx",
    "ĝ": "gx",
    "ĥ": "hx",
    "ĵ": "jx",
    "ŝ": "sx",
    "ŭ": "ux",
    "Ĉ": "Cx",
    "Ĝ": "Gx",
    "Ĥ": "Hx",
    "Ĵ": "Jx",
    "Ŝ": "Sx",
    "Ŭ": "Ux",
}

def x_igi(teksto):
    rez = teksto
    for diakritajxo, anstatauxo in sendiakritigi.items():
        rez = rez.replace(diakritajxo, anstatauxo)
    return rez

def sen_x_igi(teksto):
    rez = teksto
    for diakritajxo, anstatauxo in sendiakritigi.items():
        rez = rez.replace(anstatauxo, diakritajxo)
    rez = (
        rez.replace("CX", "Ĉ")
        .replace("GX", "Ĝ")
        .replace("HX", "Ĥ")
        .replace("JX", "Ĵ")
        .replace("SX", "Ŝ")
        .replace("UX", "Ŭ")
    )
    return rez

class CelDosiero:
    """Файл для записи"""

    def __init__(self, dvojo, encoding="utf-8", formatilo=sen_x_igi):
        self.dvojo = dvojo
        self.encoding = encoding
        self.formatilo = formatilo

    def skribi(self, teksto):
        with open(self.dvojo, "w", encoding=self.encoding) as dosiero:
            dosiero.write(self.formatilo(teksto))

    def skribi_liniojn(self, linioj):
        output = "\n".join(linioj)
        self.skribi(output)

    def skribi_vortliston(self, vortoj):
        self.skribi_liniojn(vortoj)

    def skribi_dict(self, dic, sep="\t"):
        self.skribi_liniojn([f"{key}{sep}{val}" for key, val in dic.items()])
