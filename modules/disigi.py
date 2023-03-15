import re
from functools import reduce

from .dosierojn_ls import FontDosiero, CelDosiero, x_igi, DATA_DIR
from .lingvaj_konstantoj import MORFEMARO, LEKSEMARO, VORTETOJ
from .utils import senfinajxigi, forigi_ripetojn_konservante_ordon
from .vortaro import BAZA_VORTARO

# Виды морфем
EO_BASE = {'Va': VORTETOJ.Va, # VORTETOJ - слова, которые не требуют окончания
           'Vp': VORTETOJ.Vp,
           'Vpl': VORTETOJ.Vpl,
           'Vpa': VORTETOJ.Vpa,
           'Vr': VORTETOJ.Vr,
           'N': [], # Арабские числа # Специальные разбор в функции dividi
           'F': MORFEMARO.finajxoj, # Окончания
           'A': MORFEMARO.afiksoj, # Аффиксы
           'K': MORFEMARO.internaj_literaj_kunligajxoj, # Соединительная гласная или символ
           'S': MORFEMARO.internaj_kunligaj_simboloj, # дефис
           'R': [] # Возможные корни из словаря # EO_BASE['R'] инициализируется внутри класса Dismorfemo
           }
EO_REGULOJ = {'w': ['N', 'Vr', 'Vp', 'Vpl', 'Vpa', 'Va'] + ['aF', 'bVr'], # начальное состояние
              'a': ['N', 'R', 'A', 'Vr', 'Vp', 'Vpa'] + ['bR', 'bA', 'bVr'] + ['dS'], # состояние после окончания
              'b': ['N', 'R', 'A', 'Vr', 'Vp', 'Vpl'] + ['bR', 'bA', 'bVr'] + ['cK', 'dS'], # сосотояние после корня или корнеподобной морфемы
              'c': ['N', 'R', 'A', 'Vr', 'Vp', 'Vpl'] + ['bR', 'bA', 'bVr'], # состояние после соединительной гласной
              'd': ['N', 'R', 'A', 'Vr', 'Vp', 'Vpl', 'Vpa', 'Va'] + ['aF', 'bR', 'bA', 'bVr'] # состояние поcле дефиса
              }

# Вес морфемы каждого типа
def PEZO(x):
    if x in ['F']:
        return 1
    elif x in ['A', 'Va']:
        return 5
    elif x in ['K', 'S']:
        return 7
    else:
        return 10

class Gramatiko:
    """ Леволинейная грамматика для распознавания слов языка
    
    Все нетерминальные символы бывают двух видов: состояния и множества.
    Символы-состояния обозначаются строчными латинскими буквами, а символы-множества --- строками, начинающимися с заглавной буквы.
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
        if regulo[0].islower():
            new_state = regulo[0]
            tipo = regulo[1:]
        else:
            new_state = ''
            tipo = regulo
        variantoj = []
        sxablonoj = [f'{mor}$' for mor in self.base[tipo]] if tipo != 'N' else ['\d+$']
        for sxablono in sxablonoj:
            match = re.search(sxablono, peco)
            if match:
                left_peco = peco[:match.start()]
                if (new_state != '' and left_peco != '') or (new_state == '' and left_peco == ''):
                    rez = ((left_peco, new_state), (match[0], tipo))
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
    def __init__(self, vorto, maksimuma_nombro_de_disigoj = 2):
        self.vorto = vorto.lower()
        self.radikalo = self.ricevi_radikalon() # основа слова
        self.eblaj_radikoj = self.ricevi_eblajn_radikojn()
        self.gramatiko = self.ricevi_tauxgan_gramatikon()
        
        self.senlimigaj_disigoj = self.gramatiko.disigi(self.vorto)
        self.senlimigaj_disigoj.sort(key = Dismorfemo.pezo)
        self.disigoj = self.senlimigaj_disigoj[:maksimuma_nombro_de_disigoj]
        
        self.radikoj = self.ricevi_radikojn()
    
    @staticmethod
    def pezo(disigo):
        return reduce(lambda x, y: x + y, map(lambda x: PEZO(x[1]), disigo))
    
    def ricevi_tauxgan_gramatikon(self):
        baseR = dict(EO_BASE)
        baseR['R'] = self.eblaj_radikoj
        return Gramatiko(base = baseR)
    
    def __str__(self):
        rezs = []
        for disigo in self.senlimigaj_disigoj:
            out = '-'.join(filter(lambda x: x != '-', map(lambda x: x[0], disigo)))
            rezs.append(out + f'({Dismorfemo.pezo(disigo)})')
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
    
    
