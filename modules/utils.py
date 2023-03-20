import re


def senfinajxigi(vorto, finajxoj, esceptoj=[]):
    """Удалить окончание у слова vorto

    Args:
        finajxoj: возможные окончания
        esceptoj: слова-исключения
    """

    if vorto in esceptoj:
        return vorto
    else:
        sxablono = "|".join(map(lambda w: f"{w}$", finajxoj))
        return re.split(sxablono, vorto)[0]


def forigi_ripetojn_konservante_ordon(listo):
    """Возвращает список, полученный из списка listo удалением повторяющихся элементов. При этом исходный порядок элементов списка listo сохраняется"""
    rezulto = []
    for elemento in listo:
        if elemento not in rezulto:
            rezulto.append(elemento)
    return rezulto


def listo_sen_certaj_elementoj(listo, elementoj):
    """Возвратить список, полученный из списка listo удалением элементов, присутствующих в списке elementoj."""
    return [x for x in listo if x not in elementoj]
