from itertools import product

from .utils import forigi_ripetojn_konservante_ordon

class Morfemaro:
    def __init__(self):
        # Окончания
        self.ordinaraj_vortaraj_finajxoj = ['o', 'a', 'i', 'e']
        self.vortaraj_finajxoj = self.ordinaraj_vortaraj_finajxoj + ['-', 'oj', 'aj'] # Окончания у слов в словарном виде
        #self.postfinajxoj = ['j', 'jn', 'n']
        self.jn_finajxoj = ['oj', 'ojn', 'on', 'aj', 'ajn', 'an'] + ['en']
        self.verbaj_senvortaraj_finajxoj = ['is', 'as', 'os', 'us', 'u']
        self.finajxoj = self.ordinaraj_vortaraj_finajxoj + self.jn_finajxoj + self.verbaj_senvortaraj_finajxoj + ["'"]
        
        # Аффиксы
        self.oficialaj_sufiksoj = ['acx', 'ad', 'ajx', 'an', 'ant', 'ar', 'at',
                                   'ebl', 'ec', 'eg', 'ej', 'em', 'end', 'er', 'estr', 'et',
                                   'id', 'ig', 'igx', 'il', 'in', 'ind', 'ing', 'int', 'ism', 'ist', 'it',
                                   'obl', 'on', 'ont', 'op', 'ot',
                                   'uj', 'ul', 'um']
        self.karesaj_sufiksoj = ['cxj', 'nj']
        self.neoficialaj_sufiksoj = ['ac', 'al', 'ed', 'esk', 'i', 'icx', 'ik', 'iv', 'iz', 'ol', 'oz', 'uk', 'unt', 'ut']
        self.sufiksoj = self.oficialaj_sufiksoj
        self.prefiksoj = ['bo', 'dis', 'ek', 'eks', 'ge', 'mal', 'mis', 'pra', 're'] # oficialaj
        self.afiksoj = self.sufiksoj + self.prefiksoj
MORFEMARO = Morfemaro()

def produto(list1, list2):
    """Список полученный попарной конкатенацией всех элементов из списоков list1 и list2"""
    return list(map(lambda x: ''.join(x), product(list1, list2)))

class Leksemaro:
    def __init__(self):
        # Табличные слова (включая kien, tien, cxien и т.п.)
        self.tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['a', 'al', 'am', 'e', 'el', 'en', 'es', 'o', 'om', 'u', 'en'])
        self.o_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['o'])
        self.au_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['a', 'u'])
        self.oau_tabelvortoj = self.o_tabelvortoj + self.au_tabelvortoj
        self.es_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['es'])
        self.e_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['e'])
        self.en_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['en'])
        self.am_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['am'])
        self.alelom_tabelvortoj = produto(['ki', 'ti', 'i', 'cxi', 'neni'], ['al', 'el', 'om'])
        self.jn_tabelvortoj = produto(self.o_tabelvortoj, ['n']) + produto(self.au_tabelvortoj, ['j', 'jn', 'n'])
        
        # Местоимения
        self.pronomoj = ['mi', 'ni', 'vi', 'ci', 'li', 'sxi', 'gxi', 'ili', 'oni', 'si']
        self.n_pronomoj = produto(self.pronomoj, ['n'])
        # Предлоги
        self.rolvortetoj = ['al', 'anstataux', 'antaux', 'apud', 'cxe', 'cxirkaux', 'da', 'de', 'dum', 'ekster', 'el', 'en',
                            'gxis', 'inter', 'je', 'kontraux', 'krom', 'kun', 'laux', 'malgraux',
                            'per', 'po', 'por', 'post', 'preter', 'pri', 'pro', 'sen', 'sub', 'super', 'sur', 'tra', 'trans']
        # Числовые слова
        self.nombraj_vortetoj = ['unu', 'du', 'tri', 'kvar', 'kvin', 'ses', 'sep', 'ok', 'naux', 'dek', 'cent', 'mil', 'nul']
        # Союзы
        self.kunligaj_vortetoj = ['kaj', 'aux', 'sed', 'plus', 'minus', 'nek'] # konjunkcioj
        self.frazenkondukaj_vortetoj = ['ke', 'cxu', 'se', 'cxar', 'apenaux', 'dum', 'gxis', 'kvankam', 'kvazaux', 'ol'] # subjunkcioj
        self.konjunkcioj = self.kunligaj_vortetoj + self.frazenkondukaj_vortetoj
        # Сравнительные частицы
        self.komparaj_vortetoj = ['kiel', 'ol']
        # O-vortecaj kaj A-vortecaj vortetoj
        self.oa_vortecaj_vortetoj = self.oau_tabelvortoj + self.es_tabelvortoj + ['la', 'ambaux']
        # E-vortecaj vortetaj
        self.e_lokaj_vortetoj = self.e_tabelvortoj + ['cxi', 'for']
        self.en_lokaj_vortetoj = self.en_tabelvortoj
        self.e_tempaj_vortetoj = self.am_tabelvortoj + ['ankoraux', 'baldaux', 'hodiaux', 'hieraux', 'morgaux', 'jam', 'jxus', 'nun', 'plu','tuj']
        self.e_diversaj_vortetoj = self.alelom_tabelvortoj + ['ajn', 'almenaux', 'ankaux', 'apenaux', 'des', 'do', 'ecx', 'ja', 'jen', 'jes', 'ju', 'kvazaux', 'mem', 'ne', 'nur', 'pli', 'plej', 'preskaux', 'tamen', 'tre', 'tro']
        self.e_vortetoj = self.e_lokaj_vortetoj + self.en_lokaj_vortetoj + self.e_tempaj_vortetoj + self.e_diversaj_vortetoj
        # Звукоподражания
        self.ekkriaj_vortetoj = ['adiaux', 'bis', 'fi', 'ha', 'he', 'ho', 'hura', 'nu', 've']
        
        # Классы для vortetoj
        self.jn_vortetoj = self.jn_tabelvortoj + self.n_pronomoj
        self.cxiuj_vortetoj = self.pronomoj + self.rolvortetoj + self.nombraj_vortetoj + self.konjunkcioj + self.komparaj_vortetoj +\
            self.oa_vortecaj_vortetoj + self.e_vortetoj + self.ekkriaj_vortetoj
        self.cxiuj_vortetoj = forigi_ripetojn_konservante_ordon(self.cxiuj_vortetoj)
        
        # Цифры
        self.nombroj = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LEKSEMARO = Leksemaro()
