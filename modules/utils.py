import re

def senfinajxigi(vorto, finajxoj, esceptoj):
    """Удалить окончание у слова vorto
    
    finajxoj - возможные окончания
    esceptoj - слова-исключения
    """
    
    if vorto in esceptoj:
        return vorto
    else:
        sxablono = '|'.join(map(lambda w: f'{w}$', finajxoj))
        return re.split(sxablono, vorto)[0]

def forigi_ripetojn_konservante_ordon(listo):
    """Удалить повторения, сохраняя порядок элементов в списке"""
    rezulto = []
    for elemento in listo:
        if elemento not in rezulto:
            rezulto.append(elemento)
    return rezulto
                
