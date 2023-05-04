"""
    Функции для преобразования текста на эсперанто из одного формата в другой.
    
    Подерживаются два формата:
    1) нормальный (с диакритическими знаками)
    2) суррогатный (используется вспомогательный символ x)
"""

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
