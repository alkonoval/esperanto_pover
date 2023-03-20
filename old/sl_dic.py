def legi_sublinio_dic(dnomo, sep, encoding="ibm866"):
    """Считать файл типа .dic для программы Sublinio и возвратить словарь {'signifo' : dic_signifo, 'tipo': dic_tip, 'nivelo': dic_nivelo}

    Оригинальные .dic-файлы для программы Sublinio имеют кодировку ibm866
    В файле sufikso.dic и prefikso.dic в качестве sep надо использовать '#'
    В файле cxefa.dic в качестве sep надо использовать '\t'

    dic_signifo
    Словарь: морфема (корень/суффикс/преффикс) -> ее значение (перевод, комментарий)

    dic_tip
    Словарь: морфема (корень/суффикс/преффикс) -> ее тип (может ли суффикс оканчивать слово? "." - да, <пусто> - нет, ":" - да или нет)
    Возможные типы:
    '' (пустое слово) - слово не может заканчиваться морфемой, требуется добавить окончание или суффикс
                        (например: "libr": "libro" - книга)
    '.' - морфема представляет собой самостоятельное слово, к которому недопустимо прибалять окончание
          (например: al, do, cxar)
    ':' - морфема представляет собой самостоятельное слово и без окончание, однако для образования слова допустимо добавить окончание
         (например, "dek": "dek" - "десять", "deka" - "десятый");


    dic_nivelo
    Словарь: морфема (корень/суффикс/преффикс) -> ее уровень (насколько морфема может ближе к окончанию относительно других морфем)
    Морфемы уровня n+1 не могут располагать ближе к окончанию слова чем морфемы уровня n.
    """

    dosiero = open(dnomo, "r", encoding=encoding)
    rezulto = {"signifo": {}, "tipo": {}, "nivelo": {}}
    for row in dosiero.readlines():
        split = row.split(sep, maxsplit=1)
        key = split[0].strip()
        if not key:
            continue
        # Находим value
        value = split[1].split("#")[0].strip() if len(split) > 1 else ""
        # Находим nivelo
        nivelo = 0
        if key[0].isdigit():
            nivelo = int(key[0])
            key = key[1:]
            if not key:
                continue
        # Находим tipo
        tipo = ""
        if key[-1] in [".", ":"]:
            tipo = key[-1]
            key = key[:-1]
            if not key:
                continue
        # Добавляем value, nivelo, tipo в словари
        rezulto["signifo"][key] = value
        rezulto["nivelo"][key] = nivelo
        rezulto["tipo"][key] = tipo
    dosiero.close()
    return rezulto


def ricevi_senfinajxaj_vortoj():
    el_radikoj = legi_sublinio_dic(dnomo="cxefa.dic", sep="\t")
    tutaj_sb_radikoj = el_radikoj["signifo"].keys()
    # ordinaraj_radikoj = list(filter(lambda rad: el_radikoj['tipo'][rad] == '', tutaj_sb_radikoj))
    memvortaj_radikoj = list(
        filter(lambda rad: el_radikoj["tipo"][rad] == ".", tutaj_sb_radikoj)
    )
    kompleksaj_radikoj = list(
        filter(lambda rad: el_radikoj["tipo"][rad] == ":", tutaj_sb_radikoj)
    )
    senfinajxaj_vortoj = (
        memvortaj_radikoj + kompleksaj_radikoj
    )  # Слова, у которых в словарном виде нет окончания
    return senfinajxaj_vortoj


def ricevi_sufiksoj():
    sufiksoj = list(
        filter(
            lambda rad: sb_sufiksoj["nivelo"][rad] == 3, sb_sufiksoj["signifo"].keys()
        )
    )
    return sufiksoj


def ricevi_prefiksoj():
    prefiksoj = list(legi_sublinio_dic(dnomo="prefikso.dic", sep="#")["signifo"].keys())
    return prefiksoj


if __name__ == "__main__":
    pass
