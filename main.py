from argparse import ArgumentParser
from pathlib import Path

from modules.teksto import Teksto

TESTTEXT = Path(__file__).parent / "input" / "Teksto.txt"
def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "filename",
        help="Имя файла с текстом для обработки. Должен быть в кодировке Unicode (UTF-8)",
        type=Path,
        default=TESTTEXT,
        nargs="?",  # argument is optional
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    OUTPUT_DIR = Path("./output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    teksto = Teksto().elsxuti_el_dosieron(dvojo=args.filename)
    teksto.prilabori()

    # Сохранить морфологический разбор всех слов текста
    teksto.skribi_dismorfigon(dvojo = OUTPUT_DIR / "Dismorfemo")
    teksto.skribi_dismorfigon(dvojo = OUTPUT_DIR / "Dismorfemo_plendetala", plendetala=True)

    # Получить словарик для слов из текста
    teksto.vortareto.save(dvojo = OUTPUT_DIR / "Vortareto")

    # Сохранить словарные слова
    teksto.skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(
        OUTPUT_DIR / "Vortaraj_vortoj_rilate_al_origignaj_vortoj.txt"
    )
