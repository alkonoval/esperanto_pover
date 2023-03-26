import re
from functools import reduce

from .dosierojn_ls import x_igi, sen_x_igi
from .lingvaj_konstantoj import LEKSEMARO, MORFEMARO, VORTETOJ, rafini_vorton
from .utils import forigi_ripetojn_konservante_ordon, senfinajxigi
from .vortaro import BAZA_VORTARO


class VortEoGramatiko:
    """
    Леволинейная пораждающая грамматика слов языка Эсперанто

    Все нетерминальные символы бывают двух видов: состояния и множества.

    Символы-состояния обозначаются строчными латинскими буквами, а символы-
    множества --- строками, начинающимися с заглавной буквы.

    Правила бывают двух видов:

    1) Определяется словаряем morfemoj : tipo -> [str1, str2, ..., str_n], который
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

    Attributes
        radikoj: iterable - список базовых словарных корней
    """
    
    def __init__(self, radikoj):
        # Словарь: морфемный тип -> список морфем данного типа
        self.morfemoj = {
            # VORTETOJ - слова, которые не требуют окончания
            "Va": VORTETOJ.Va,
            "Vp": VORTETOJ.Vp,
            "Vpl": VORTETOJ.Vpl,
            "Vpa": VORTETOJ.Vpa,
            "Vr": VORTETOJ.Vr,
            # Арабские числа # Специальные разбор в функции VortEoGramatiko._dividi
            "N": None,
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
            "R": radikoj,
        }
        self.start = "w"
        self.reguloj = {
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

    def _dividi(self, peco, regulo):
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
        sxablonoj = [f"{mor}$" for mor in self.morfemoj[tipo]] if tipo != "N" else ["\d+$"]
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
            rez = self._dividi(peco, regulo)
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
    """ Представление разбора слова на морфемы в виде: [(mor_1, tip_n), ..., (mor_n, tip_n)],
    где mor_1, ..., mor_n - морфемы (части слова),
    а tip_1, ..., tip_2 - соответствующие тыпы морфемы из VortEoGramatiko.morfemoj.keys()
    """

    # Вес морфемы каждого типа
    morfem_pezo = {
            "R": 10, # корень
            "N": 10, # число (арабскими цифрами)
            "F": 1, # окончание
            "Ap": 4, # приставки
            "As": 4, # суффиксы
            "K": 3, # соеднитительная гласная
            "S": 3, # дефис
            # Подтипы специальных слов-корней из VORTETOJ, которые не требуют окончания
            "Va": 4, 
            "Vp": 10,
            "Vpl": 10,
            "Vpa": 4,
            "Vr": 9,
        }

    def __str__(self):
        """ mor_1-mor_2-...-mor_n """
        return "-".join(filter(lambda x: x != "-", map(lambda paro: sen_x_igi(paro[0]), self)))
    
    def pezo(self):
        """ Получить вес разбора слова.
            Разборы слова, которые имееют меньший вес, считаются более "правильными".
        """
        # Сумма весов морфем
        rezulto = reduce(lambda x, y: x + y, map(lambda x: self.morfem_pezo[x[1]], self))
        # Штраф за расположение морфем
        puno = 0
        # Если слово начинается с суффикса, то вес этого суффикса дополняется до веса корня
        puno += self.morfem_pezo['R'] - self.morfem_pezo['As'] if self[0][1] == 'As' else 0
        rezulto += puno
        return rezulto 
    
    def ricevi_morfemojn(self, kondicho_por_morfema_tipo):
        return [x[0] for x in self if kondicho_por_morfema_tipo(x[1])]

class Dismorfemo:
    """ Разборы слова на морфемы """

    def __init__(
        self, vorto, cxiuj_vortaraj_radikoj = BAZA_VORTARO.radikoj(output_format="set")
        ):
        # Слово для морфологического разбора
        self.vorto = x_igi(vorto.lower())
        # Основа слова
        self.radikalo = senfinajxigi(
            self.vorto, finajxoj=MORFEMARO.finajxoj, esceptoj=LEKSEMARO.cxiuj_vortetoj
        )
        # Все подстроки слова, которые встречаются в множестве cxiuj_vortaraj_radikoj
        self.eblaj_radikoj = self._ricevi_eblajn_radikojn(cxiuj_vortaraj_radikoj)
        # Порождающая грамматика, посредством которой будет производиться разбор слова
        self.gramatiko = VortEoGramatiko(radikoj=self.eblaj_radikoj)
        self.senlimigaj_disigoj = self.gramatiko.disigi(self.vorto)
        if self.senlimigaj_disigoj != []:
            # Все возможные разборы слова на морфемы, упорядоченные по весу
            self.senlimigaj_disigoj = list(map(Disigo, self.senlimigaj_disigoj))
            self.senlimigaj_disigoj.sort(key=lambda x: x.pezo())
            min_pezo = self.senlimigaj_disigoj[0].pezo()
            # Лучшие разборы слова (разборы с наименьшим весом)
            self.disigoj = list(filter(lambda x: x.pezo() == min_pezo, self.senlimigaj_disigoj))
        else:
            # Слово не имеет разборов
            self.disigoj = []
        self.radikoj = self.ricevi_morfemojn(lambda tipo: tipo == "R")
        self.vortetoj = self.ricevi_vortetojn()
    
    def _ricevi_eblajn_radikojn(self, vortaraj_radikoj):
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

    def __str__(self):
        rezs = []
        for disigo in self.senlimigaj_disigoj:
            rezs.append(f"{disigo}({disigo.pezo()})")
        return ", ".join(rezs)

    def ricevi_morfemojn(self, kondicho_por_morfema_tipo):
        """
        Получить список морфем из разбора, тип которых удовлетворяет уcловию
        kondicho_por_morfema_tipo

        Args:
            kondicho_por_morfema_tipo: одноместная функция из множества
            VortEoGramatiko.morfemoj.keys() в bool
        """
        rezulto = []
        for disigo in self.disigoj:
            morfemoj = [x[0] for x in disigo if kondicho_por_morfema_tipo(x[1])]
            rezulto += morfemoj
        return rezulto

    def ricevi_vortetojn(self):
        """
        Получить все специальные слова, встречающиеся в разборе. При этом
        удаляются постокончания -j, -n, -jn.
        """
        vortetoj = self.ricevi_morfemojn(lambda x: x[0] == "V")
        rafinitaj_vortetoj = list(map(rafini_vorton, vortetoj))
        return forigi_ripetojn_konservante_ordon(rafinitaj_vortetoj)