from itertools import product
from functools import reduce

from .utils import (
    forigi_ripetojn_konservante_ordon,
    listo_sen_certaj_elementoj,
    senfinajxigi,
)


def produto(list1, list2):
    """Список полученный попарной конкатенацией всех элементов из списоков list1 и list2"""
    return list(map(lambda x: "".join(x), product(list1, list2)))


class Morfemaro:
    def __init__(self):
        # Окончания
        self.ordinaraj_vortaraj_finajxoj = ["o", "a", "i", "e"]
        self.vortaraj_finajxoj = self.ordinaraj_vortaraj_finajxoj + [
            "-",
            "!",
            "oj",
            "aj",
        ]  # Окончания у слов в словарном виде
        self.postfinajxoj = ["j", "jn", "n"]
        self.jn_finajxoj = produto(["o", "a"], self.postfinajxoj) + ["en"]
        self.verbaj_senvortaraj_finajxoj = ["is", "as", "os", "us", "u"]
        self.finajxoj = (
            self.ordinaraj_vortaraj_finajxoj
            + self.jn_finajxoj
            + self.verbaj_senvortaraj_finajxoj
            + ["'"]
        )

        # Соединительная гласная/символ внутри слова
        self.internaj_literaj_kunligajxoj = ["o", "e", "en", "i", "a"]
        self.internaj_kunligaj_simboloj = ["-"]

        # Аффиксы
        self.oficialaj_sufiksoj = [
            "acx",
            "ad",
            "ajx",
            "an",
            "ant",
            "ar",
            "at",
            "ebl",
            "ec",
            "eg",
            "ej",
            "em",
            "end",
            "er",
            "estr",
            "et",
            "id",
            "ig",
            "igx",
            "il",
            "in",
            "ind",
            "ing",
            "int",
            "ism",
            "ist",
            "it",
            "obl",
            "on",
            "ont",
            "op",
            "ot",
            "uj",
            "ul",
            "um",
        ]
        self.karesaj_sufiksoj = ["cxj", "nj"]
        # self.neoficialaj_sufiksoj = ['ac', 'al', 'ed', 'esk', 'i', 'icx', 'ik', 'iv', 'iz', 'ol', 'oz', 'uk', 'unt', 'ut']
        self.sufiksoj = self.oficialaj_sufiksoj
        self.prefiksoj = [
            "bo",
            "dis",
            "ek",
            "eks",
            "ge",
            "mal",
            "mis",
            "pra",
            "re",
            "fi",
        ]  # oficialaj
        self.afiksoj = self.sufiksoj + self.prefiksoj


MORFEMARO = Morfemaro()


class Leksemaro:
    def __init__(self):
        # Табличные слова (включая kien, tien, cxien и т.п.)
        self.tabelvortoj = produto(
            ["ki", "ti", "i", "cxi", "neni"],
            ["a", "al", "am", "e", "el", "en", "es", "o", "om", "u"],
        )
        self.o_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["o"])
        self.au_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["a", "u"])
        self.oau_tabelvortoj = self.o_tabelvortoj + self.au_tabelvortoj
        self.ne_oau_om_tabelvortoj = produto(
            ["ki", "ti", "i", "cxi", "neni"], ["al", "am", "e", "el", "en", "es"]
        )
        self.es_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["es"])
        self.e_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["e"])
        self.en_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["en"])
        self.am_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["am"])
        self.om_tabelvortoj = produto(["ki", "ti", "i", "cxi", "neni"], ["om"])
        self.alelom_tabelvortoj = produto(
            ["ki", "ti", "i", "cxi", "neni"], ["al", "el", "om"]
        )
        self.jn_tabelvortoj = (
            produto(self.o_tabelvortoj, ["n"])
            + produto(self.au_tabelvortoj, ["j", "jn", "n"])
            + self.en_tabelvortoj
        )

        # Местоимения
        self.pronomoj = ["mi", "ni", "vi", "ci", "li", "sxi", "gxi", "ili", "oni", "si"]
        self.n_pronomoj = produto(self.pronomoj, ["n"])
        # Предлоги
        self.rolvortetoj = [
            "al",
            "anstataux",
            "antaux",
            "apud",
            "cxe",
            "cxirkaux",
            "da",
            "de",
            "dum",
            "ekster",
            "el",
            "en",
            "gxis",
            "inter",
            "je",
            "kontraux",
            "krom",
            "kun",
            "laux",
            "malgraux",
            "per",
            "po",
            "por",
            "post",
            "preter",
            "pri",
            "pro",
            "sen",
            "sub",
            "super",
            "sur",
            "tra",
            "trans",
        ]
        # Числовые слова
        self.nombraj_vortetoj = [
            "unu",
            "du",
            "tri",
            "kvar",
            "kvin",
            "ses",
            "sep",
            "ok",
            "naux",
            "dek",
            "cent",
            "mil",
            "nul",
        ]
        # Союзы
        self.kunligaj_vortetoj = [
            "kaj",
            "aux",
            "sed",
            "plus",
            "minus",
            "nek",
        ]  # konjunkcioj
        self.frazenkondukaj_vortetoj = [
            "ke",
            "cxu",
            "se",
            "cxar",
            "apenaux",
            "dum",
            "gxis",
            "kvankam",
            "kvazaux",
            "ol",
        ]  # subjunkcioj
        self.konjunkcioj = self.kunligaj_vortetoj + self.frazenkondukaj_vortetoj
        # Сравнительные частицы
        self.komparaj_vortetoj = ["kiel", "ol"]
        # O-vortecaj kaj A-vortecaj vortetoj
        self.oa_vortecaj_vortetoj = (
            self.oau_tabelvortoj + self.es_tabelvortoj + ["la", "ambaux"]
        )
        # E-vortecaj vortetaj
        self.e_lokaj_vortetoj = self.e_tabelvortoj + ["cxi", "for"]
        self.en_lokaj_vortetoj = self.en_tabelvortoj
        self.e_tempaj_vortetoj = self.am_tabelvortoj + [
            "ankoraux",
            "baldaux",
            "hodiaux",
            "hieraux",
            "morgaux",
            "jam",
            "jxus",
            "nun",
            "plu",
            "tuj",
        ]
        self.e_diversaj_vortetoj = self.alelom_tabelvortoj + [
            "ajn",
            "almenaux",
            "ankaux",
            "apenaux",
            "des",
            "do",
            "ecx",
            "ja",
            "jen",
            "jes",
            "ju",
            "kvazaux",
            "mem",
            "ne",
            "nur",
            "pli",
            "plej",
            "preskaux",
            "tamen",
            "tre",
            "tro",
        ]
        self.e_vortetoj = (
            self.e_lokaj_vortetoj
            + self.en_lokaj_vortetoj
            + self.e_tempaj_vortetoj
            + self.e_diversaj_vortetoj
        )
        # Звукоподражания
        self.ekkriaj_vortetoj = ["adiaux", "bis", "ha", "he", "ho", "hura", "nu", "ve"]

        self.vortetoj = (
            self.pronomoj
            + self.rolvortetoj
            + self.nombraj_vortetoj
            + self.konjunkcioj
            + self.komparaj_vortetoj
            + self.oa_vortecaj_vortetoj
            + self.e_vortetoj
            + self.ekkriaj_vortetoj
        )
        self.vortetoj = forigi_ripetojn_konservante_ordon(
            self.vortetoj
        )  # включая kien, tien и т.п.

        self.jn_vortetoj = self.jn_tabelvortoj + self.n_pronomoj
        self.ne_jn_vortetoj = listo_sen_certaj_elementoj(
            self.vortetoj, self.jn_vortetoj
        )
        self.cxiuj_vortetoj = self.ne_jn_vortetoj + self.jn_vortetoj

        # Цифры
        self.ciferoj = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


LEKSEMARO = Leksemaro()


def rafini_vorton(vorto):
    """Удаляет постокончание -j, -n, -jn"""
    return senfinajxigi(
        vorto, finajxoj=MORFEMARO.postfinajxoj, esceptoj=LEKSEMARO.ne_jn_vortetoj
    )


class Vortetoj:
    """
    Специальные слова (слова, могущие употребляться без окончания)

    Поля:
    Va --- специальные слова, которые употребляются только отдельно (не могут быть частью составного слова)
    Vp --- специальные слова, которые употреблятся только в начале сложного слова, справа к ним может присоединяться любая морфема
    Vpl --- специальные слова, которые употреблятся только в начале сложного слова, справа не может присоединяться окончание
    Vpa --- специальные слова, которые употреблятся только в начале сложного слова, справа может присоединяться только окончание
    Vr --- специальные слова, которые могут быть в начале, конце и ввнутри сложного слова
    """

    def __init__(self):
        self.Va = (
            LEKSEMARO.jn_tabelvortoj
            + LEKSEMARO.n_pronomoj
            + [
                "ke",
                "cxu",
                "se",
                "cxar",
                "ol",
                "la",
                "cxi",
                "da",
                "je",
                "malgraux",
                "kvankam",
                "nek",
                "des",
                "do",
                "ja",
                "ju",
            ]
        )
        self.Vpa = (
            LEKSEMARO.pronomoj
            + ["kaj", "aux", "sed", "plus", "minus"]
            + ["po", "ecx"]
            + LEKSEMARO.ekkriaj_vortetoj
            + LEKSEMARO.ne_oau_om_tabelvortoj
        )
        self.Vpl = LEKSEMARO.oau_tabelvortoj
        self.Vp = LEKSEMARO.om_tabelvortoj + ["ajn"]
        self.Vr = LEKSEMARO.nombraj_vortetoj + [
            "al",
            "anstataux",
            "antaux",
            "apud",
            "cxe",
            "cxirkaux",
            "de",
            "dum",
            "ekster",
            "el",
            "en",
            "gxis",
            "inter",
            "kontraux",
            "krom",
            "kun",
            "laux",
            "per",
            "por",
            "post",
            "preter",
            "pri",
            "pro",
            "sen",
            "sub",
            "super",
            "sur",
            "tra",
            "trans",
            "ambaux",
            "ankoraux",
            "baldaux",
            "hodiaux",
            "hieraux",
            "morgaux",
            "jam",
            "jxus",
            "nun",
            "plu",
            "tuj",
            "almenaux",
            "ankaux",
            "apenaux",
            "jen",
            "jes",
            "kvazaux",
            "mem",
            "ne",
            "nur",
            "pli",
            "plej",
            "preskaux",
            "tamen",
            "tre",
            "tro",
            "for",
        ]

        # vorteto -> tipo (Va, Vr и т.п.)
        speco = {}
        for nomo, listo in self.__dict__.items():
            speco.update([(x, nomo) for x in listo])
        self.speco = speco

        self.cxiuj = list(self.speco.keys())


VORTETOJ = Vortetoj()
