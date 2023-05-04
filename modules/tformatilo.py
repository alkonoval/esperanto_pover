"""Чтение и запись файлов"""

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
