"""Чтение и запись файлов"""

diakritajxoj = ["ĉ", "ĝ", "ĥ", "ĵ", "ŝ", "ŭ"]
Diakritajxoj = ["Ĉ", "Ĝ", "Ĥ", "Ĵ", "Ŝ", "Ŭ"]

def x_igi(teksto):
    rez = teksto
    rez = (
        rez.replace("ĉ", "cx")
        .replace("ĝ", "gx")
        .replace("ĥ", "hx")
        .replace("ĵ", "jx")
        .replace("ŝ", "sx")
        .replace("ŭ", "ux")
    )
    rez = (
        rez.replace("Ĉ", "Cx")
        .replace("Ĝ", "Gx")
        .replace("Ĥ", "Hx")
        .replace("Ĵ", "Jx")
        .replace("Ŝ", "Sx")
        .replace("Ŭ", "Ux")
    )
    return rez


def sen_x_igi(teksto):
    rez = teksto
    rez = (
        rez.replace("cx", "ĉ")
        .replace("gx", "ĝ")
        .replace("hx", "ĥ")
        .replace("jx", "ĵ")
        .replace("sx", "ŝ")
        .replace("ux", "ŭ")
    )
    rez = (
        rez.replace("Cx", "Ĉ")
        .replace("Gx", "Ĝ")
        .replace("Hx", "Ĥ")
        .replace("Jx", "Ĵ")
        .replace("Sx", "Ŝ")
        .replace("Ux", "Ŭ")
    )
    rez = (
        rez.replace("CX", "Ĉ")
        .replace("GX", "Ĝ")
        .replace("HX", "Ĥ")
        .replace("JX", "Ĵ")
        .replace("SX", "Ŝ")
        .replace("UX", "Ŭ")
    )
    return rez


class FontDosiero:
    """Файл для чтения"""

    def __init__(self, dvojo, encoding="utf-8-sig", formatilo=x_igi):
        self.dvojo = dvojo
        self.encoding = encoding
        self.formatilo = formatilo

    def legi(self):
        """Прочитать файл, результат чтения выдать как одну большую строку"""
        with open(self.dvojo, "r", encoding=self.encoding) as dosiero:
            rezulto = self.formatilo(dosiero.read())
        return rezulto

    def legi_liniojn(self):
        """Прочитать файл, результат чтения выдать как list строк"""
        with open(self.dvojo, "r", encoding=self.encoding) as dosiero:
            rezulto = [self.formatilo(linio) for linio in dosiero.readlines()]
        return rezulto

    def legi_vortliston(self):
        """
        Считать список слов из файла. Предополается, что в файле каждое слово
        расположено на отдельной строке.
        """
        linioj = self.legi_liniojn()
        vortoj = []
        for linio in linioj:
            vorto = linio.strip()
            if vorto not in vortoj:
                vortoj.append(vorto)
        return vortoj


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
