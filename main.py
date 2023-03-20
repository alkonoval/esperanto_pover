from modules.teksto import Teksto

teksto = Teksto().elsxuti_el_dosieron(dnomo="Teksto.txt")
# teksto = Teksto().elsxuti_el_dosieron(dnomo = 'Malvarma duŝo kaj homa sano.txt')
teksto.prilabori()

# Сохранить морфологический разбор всех слов текста
teksto.skribi_dismorfigon(cel_dnomo="Dismorfemo")
teksto.skribi_dismorfigon(cel_dnomo="Dismorfemo_plendetala", plendetala=True)

# Получить словарик для слов из текста
teksto.vortareto.save(dnomo="Vortareto")

# Сохранить словарные слова
teksto.skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(
    "Vortaraj_vortoj_rilate_al_origignaj_vortoj.txt"
)
