import re
from functools import reduce

from .lingvaj_konstantoj import LEKSEMARO, MORFEMARO, VORTETOJ, rafini_vorton
from .utils import forigi_ripetojn_konservante_ordon, senfinajxigi
from .vortaro import BAZA_VORTARO

# Виды морфем
EO_BASE = {
    # VORTETOJ - слова, которые не требуют окончания
    "Va": VORTETOJ.Va,
    "Vp": VORTETOJ.Vp,
    "Vpl": VORTETOJ.Vpl,
    "Vpa": VORTETOJ.Vpa,
    "Vr": VORTETOJ.Vr,
    # Арабские числа # Специальные разбор в функции Gramatiko.dividi
    "N": [],
    # Окончания
    "F": MORFEMARO.finajxoj,
    # Приставки
    "Ap": MORFEMARO.prefiksoj,
    # Суффиксы
    "As": MORFEMARO.sufiksoj,
    # Соединительная гласная или символ
    "K": MORFEMARO.internaj_literaj_kunligajxoj,
    # дефис
    "S": MORFEMARO.internaj_kunligaj_simboloj,
    # Возможные корни из словаря
    # EO_BASE['R'] инициализируется внутри класса Dismorfemo
    "R": [],
}
EO_REGULOJ = {
    # начальное состояние
    "w": ["N", "Vr", "Vp", "Vpl", "Vpa", "Va"] + ["aF", "bVr"],
    # состояние после окончания
    "a": ["N", "R", "Ap", "As", "Vr", "Vp", "Vpa"] + ["bR", "bAs", "bAp", "bVr"] + ["dS"],
    # состояние после корня или корнеподобной морфемы
    "b": ["N", "R", "Ap", "As", "Vr", "Vp", "Vpl"] + ["bR", "bAs", "bAp", "bVr"] + ["cK", "dS"],
    # состояние после соединительной гласной
    "c": ["N", "R", "As", "Vr", "Vp", "Vpl"] + ["bR", "bAs", "bAp", "bVr"],
    # состояние поcле дефиса
    "d": ["N", "R", "Ap", "As", "Vr", "Vp", "Vpl", "Vpa", "Va"] + ["aF", "bR", "bAs", "bAp", "bVr"],
}

# Вес морфемы каждого типа
def PEZO(x):
    if x in ["F"]:
        return 1
    elif x in ["Ap", "As", "Va", "Vpa"]:
        return 5
    elif x in ["K", "S"]:
        return 5
    elif x in ["Vr"]:
        return 9
    else:
        return 10


class Gramatiko:
    """
    Леволинейная грамматика для распознавания слов языка

    Все нетерминальные символы бывают двух видов: состояния и множества.

    Символы-состояния обозначаются строчными латинскими буквами, а символы-
    множества --- строками, начинающимися с заглавной буквы.

    Правила бывают двух видов:

    1) Определяется словаряем base : X -> [str1, str2, ..., str_n], который
    каждому символу-множеству сопоставляет список строк.

    В грамматике соответствует конечному числу правил
    X -> str1, X -> str2, ..., X -> str_n

    2) Определяется словарем reguloj : x -> ['xA', 'A', 'yA', 'yB', 'B', ...],
    который каждому символу-состоянию сопоставляет список строк специального вида.

    Каждая такая строка имеет вид символ-соостояние символ-множество либо только
    символ-множество.

    В грамматике соответствует конечному числу правил
    x -> xA, x -> A, x -> yA, x -> yB, x -> B, ...

    start --- начальный нетерминальный символ-состояние
    """

    def __init__(self, base=EO_BASE, reguloj=EO_REGULOJ, start="w"):
        self.base = base
        self.reguloj = reguloj
        self.start = start

    def dividi(self, peco, regulo):
        """
        Получить все возможные варианты разбиения строки peco в соответствии со
        строкой специального вида regulo.

        Формат вывода [((left_peco, state_simbol), (right_peco, set_simblo)), ...]

        Для каждого разбиения ((left_peco, state-simbol), (right_peco, set-simblo))
        должны выполняться соотношения:

        1) left_peco + right_peco = peco

        2) Если regulo имеет вид 'xA', то
            state_simbol = 'x'
            set_simblo = 'A'
            right_peco in base['A']

        3) Если regulo имеет вид 'A', то
            left_peco = ''
            state_simbol = ''
            set_simblo = 'A'
            right_peco in base['A']
        """
        if regulo[0].islower():
            new_state = regulo[0]
            tipo = regulo[1:]
        else:
            new_state = ""
            tipo = regulo
        variantoj = []
        sxablonoj = [f"{mor}$" for mor in self.base[tipo]] if tipo != "N" else ["\d+$"]
        for sxablono in sxablonoj:
            match = re.search(sxablono, peco)
            if match:
                left_peco = peco[: match.start()]
                if (new_state != "" and left_peco != "") or (
                    new_state == "" and left_peco == ""
                ):
                    rez = ((left_peco, new_state), (match[0], tipo))
                    variantoj.append(rez)
        return variantoj

    def disigi(self, peco, state=None):
        """
        Получить все возможные разборы строки peco.

        Начальное соотояние определяется параметром state. Если этот параметром
        не задан, используется соостояние start.

        Подходящим разбором считается список вида [(s_1, A_1), ..., (s_n, A_n)],
        где s_1 ... s_n есть peco; A_1, ..., A_n --- символы-множества и строки
        s_1, ..., s_n принадлежат соответственно множествам base[A_1], ... base[A_n]
        """

        if state is None:
            state = self.start
        variantoj = []
        for regulo in self.reguloj[state]:
            rez = self.dividi(peco, regulo)
            variantoj += rez
        rezulto = []
        for vr in variantoj:
            new_peco = vr[0][0]
            new_state = vr[0][1]
            mor_kun_tipo = vr[1]
            if new_peco == "":
                rez = [mor_kun_tipo]
                rezulto.append(rez)
            else:
                rekuro = self.disigi(new_peco, new_state)
                if rekuro == []:
                    continue
                rez = []
                for it in rekuro:
                    rez.append(it + [mor_kun_tipo])
                rezulto += rez
        return rezulto

class Disigo(list):
    """ Разбор слова на морфемы в виде: [(mor_1, tip_n), ..., (mor_n, tip_n)],
    где mor_1, ..., mor_n - морфемы (части слова),
    а tip_1, ..., tip_2 - соответствующие тыпы морфемы из EO_BASE.keys()
    """
    def __str__(self):
        """ mor_1-mor_2-...-mor_n """
        return "-".join(filter(lambda x: x != "-", map(lambda x: x[0], self)))
    
    def pezo(self):
        """ Получить вес разбора слова.
            Разборы слова, которые имееют меньший вес, считаются более "правильными".
        """
        # сумма весов морфем
        rezulto = reduce(lambda x, y: x + y, map(lambda x: PEZO(x[1]), self))
        # штраф за расположение морфем
        puno = 0
        # если слово начинается с суффикса, то вес этого суффикса дополняется до веса корня
        puno += PEZO('R') - PEZO('As') if self[0][1] == 'As' else 0
        rezulto += puno
        return rezulto 
    
    def ricevi_morfemojn(self, kondicho_por_morfema_tipo):
        """
        Получить список морфем из разбора, тип которых удовлетворяет уcловию
        kondicho_por_morfema_tipo

        Args:
            kondicho_por_morfema_tipo: одноместная функция из множества
            EO_BASE.keys() в bool
        """
        return [x[0] for x in self if kondicho_por_morfema_tipo(x[1])]

class Dismorfemo:
    """ Все возможные разборы слова на морфемы """

    def __init__(self, vorto, maksimuma_nombro_de_disigoj=2):
        self.vorto = vorto.lower()
        self.radikalo = self.ricevi_radikalon()  # основа слова
        self.eblaj_radikoj = self.ricevi_eblajn_radikojn()
        self.gramatiko = self.ricevi_tauxgan_gramatikon()

        self.senlimigaj_disigoj = self.gramatiko.disigi(self.vorto)
        self.senlimigaj_disigoj = list(map(Disigo, self.senlimigaj_disigoj))
        self.senlimigaj_disigoj.sort(key=lambda x: x.pezo())
        self.disigoj = self.senlimigaj_disigoj[:maksimuma_nombro_de_disigoj]
        self.plejbona_disigo = self.disigoj[0] if self.disigoj != [] else None

        self.radikoj = self.ricevi_radikojn()
        self.vortetoj = self.ricevi_vortetojn()

    def ricevi_tauxgan_gramatikon(self):
        baseR = dict(EO_BASE)
        baseR["R"] = self.eblaj_radikoj
        return Gramatiko(base=baseR)

    def __str__(self):
        rezs = []
        for disigo in self.senlimigaj_disigoj:
            rezs.append(f"{disigo}({disigo.pezo()})")
        return ", ".join(rezs)

    def detala_info(self):
        rezulto = ""
        for key, it in self.__dict__.items():
            rezulto += f"{key} {it}\n"
        rezulto += str(self)
        return rezulto

    def ricevi_morfemojn(self, kondicho_por_morfema_tipo):
        rezulto = []
        for disigo in self.disigoj:
            morfemoj = disigo.ricevi_morfemojn(kondicho_por_morfema_tipo)
            rezulto += morfemoj
        return rezulto

    def ricevi_radikojn(self):
        return self.ricevi_morfemojn(lambda x: x == "R")

    def ricevi_vortetojn(self):
        """
        Получить все специальные слова, встречающиеся в разборе. При этом
        удаляются постокончания -j, -n, -jn.
        """
        vortetoj = self.ricevi_morfemojn(lambda x: x[0] == "V")
        rafinitaj_vortetoj = list(map(rafini_vorton, vortetoj))
        return forigi_ripetojn_konservante_ordon(rafinitaj_vortetoj)

    def ricevi_radikalon(self):
        rezulto = senfinajxigi(
            self.vorto, finajxoj=MORFEMARO.finajxoj, esceptoj=LEKSEMARO.cxiuj_vortetoj
        )
        return rezulto

    def ricevi_eblajn_radikojn(
        self, vortaraj_radikoj=BAZA_VORTARO.radikoj(output_format="set")
    ):
        rezulto = []
        vorto = self.radikalo
        esceptoj = set(LEKSEMARO.cxiuj_vortetoj + MORFEMARO.afiksoj)
        subvortoj = [
            vorto[i:j] for i in range(len(vorto)) for j in range(i + 1, len(vorto) + 1)
        ]
        for radiko in subvortoj:
            if radiko in esceptoj:
                continue
            if radiko in vortaraj_radikoj:
                rezulto.append(radiko)
        return forigi_ripetojn_konservante_ordon(rezulto)
