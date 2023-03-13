import re

from .dosierojn_ls import FontDosiero, CelDosiero, x_igi, DATA_DIR
from .konstantaro import MORFEMARO, LEKSEMARO
from .utils import senfinajxigi, forigi_ripetojn_konservante_ordon
from .vortaro import BAZA_VORTARO

EO_BASE = {'V': LEKSEMARO.cxiuj_vortetoj, # Специальные слова, могужие употребляться без окончания
           'N': LEKSEMARO.jn_vortetoj, # Специальные слова в jn-форме
           'F': MORFEMARO.finajxoj, # Окончания
           'A': MORFEMARO.afiksoj, # Аффиксы
           'G': ['o', 'e', 'en', 'i', 'a'], # Соединительная гласная
           'R': [] # Для каждого слова подставляется список возможных для него корней из словаря
        }
# Хорошо бы выделить из специальных слов те, которые 100% не могут употребляться в словообразовании, а только как самостоятельные слова
# w -> bV не для всех V (перенести такие V в N?)
# []-x то из V к чему нельзя приписовать окончания
# x-[] то из V к чему нельзя добавить приставку
EO_REGULOJ = {'w': ['V', 'bF', 'N', 'bV'],
              'b': ['V', 'R', 'A', 'bR', 'bA', 'cG'],
              'c': ['V', 'R', 'A', 'bR', 'bA']
              }

class Gramatiko:
    """ Леволинейная грамматика для распознавания слов языка
    
    Все нетерминальные символы бывают двух видов: состояния и множества.
    Символы-состояния обозначаются строчными латинскими буквами, а символы-множества --- заглавными.
    Правила бывают двух видов:
    1) Определяется словаряем base : X -> [str1, str2, ..., str_n],
    который каждому символу-множеству сопоставляет список строк.
    В грамматике соответствует конечному числу правил X -> str1, X -> str2, ..., X -> str_n
    2) Определяется словарем reguloj : x -> ['xA', 'A', 'yA', 'yB', 'B', ...],
    который каждому символу-состоянию сопоставляет список строк специального вида.
    Каждая такая строка имеет вид символ-соостояние символ-множество либо только символ-множество.
    В  грамматике соответствует конечному числу правил x -> xA, x -> A, x -> yA, x -> yB, x -> B, ...
    
    start --- начальный нетерминальный символ-состояние
    """
    def __init__(self, base = EO_BASE, reguloj = EO_REGULOJ, start = 'w'):
        self.base = base
        self.reguloj = reguloj
        self.start = start
        
    def dividi(self, peco, regulo):
        """
        Получить все возможные варианты разбиения строки peco в соответвии с строкой специального вида regulo.
        Формат вывода [((left_peco, state_simbol), (right_peco, set_simblo)), ...]
        
        Для каждого разбиения ((left_peco, state-simbol), (right_peco, set-simblo)) должны выполняться соотношения:
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
        
        tipo = regulo[-1]
        new_state = regulo[0] if len(regulo) > 1 else ''
        variantoj = []
        if new_state != '':
            for mor in self.base[tipo]:
                sxablono = f'{mor}$'
                match = re.search(sxablono, peco)
                if match:
                    left_peco = re.split(sxablono, peco)[0]
                    if left_peco != '':
                        rez = ((left_peco, new_state), (mor, tipo))
                        variantoj.append(rez)
        else:
            for mor in self.base[tipo]:
                if peco == mor:
                    rez = (('', new_state), (mor, tipo))
                    variantoj.append(rez)
        return variantoj
    
    def disigi(self, peco, state = None):
        """
        Получить все возможные разборы строки peco.
        
        Начальное соотояние определяется параметром state. Если этот параметром не задан, используется соостояние start.
        Подходящим разбором считается список вида [(s_1, A_1), ..., (s_n, A_n)], где
        s_1 ... s_n есть peco; A_1, ..., A_n --- символы-множества и
        строки s_1, ..., s_n принадлежат соответственно множествам base[A_1], ... base[A_n]
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
            if new_peco == '':
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
            
class Dismorfemo:
    def __init__(self, vorto):
        self.vorto = vorto.lower()
        self.radikalo = self.ricevi_radikalon() # основа слова
        self.eblaj_radikoj = self.ricevi_eblajn_radikojn()
        self.gramatiko = self.ricevi_tauxgan_gramatikon()
        self.disigoj = self.gramatiko.disigi(self.vorto)
        self.radikoj = self.ricevi_radikojn()
    
    def ricevi_tauxgan_gramatikon(self):
        baseR = dict(EO_BASE)
        baseR['R'] = self.eblaj_radikoj
        return Gramatiko(base = baseR)
    
    def __str__(self):
        rezs = []
        for disigo in self.disigoj:
            out = '-'.join(map(lambda x: x[0], disigo))
            rezs.append(out)
        return ', '.join(rezs)
    
    def ricevi_radikojn(self):
        rezulto = []
        for disigo in self.disigoj:
            radikoj = [x[0] for x in disigo if x[1] == 'R']
            rezulto += radikoj
        return rezulto
                        
    def ricevi_radikalon(self):
        rezulto = senfinajxigi(self.vorto, finajxoj = MORFEMARO.finajxoj, esceptoj = LEKSEMARO.cxiuj_vortetoj)
        return rezulto
    
    def ricevi_eblajn_radikojn(self, vortaraj_radikoj = BAZA_VORTARO.radikoj(output_format = 'set')):
        rezulto = []
        vorto = self.radikalo
        esceptoj = set(LEKSEMARO.cxiuj_vortetoj + MORFEMARO.afiksoj)
        subvortoj = [vorto[i:j] for i in range(len(vorto)) for j in range(i + 1, len(vorto) + 1)]
        for radiko in subvortoj:
            if radiko in esceptoj:
                continue
            if radiko in vortaraj_radikoj:
                rezulto.append(radiko)
        return forigi_ripetojn_konservante_ordon(rezulto)

if __name__ == '__main__':
    pass
    #gram = Gramatiko()
    #print(gram.disigi('malvirtulo'))
    #print(gram.disigi('persone'))
    
    #print(Dismorfemo('murmuri').disigoj)
    
    
