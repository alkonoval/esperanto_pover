import configparser
from argparse import ArgumentParser
from pathlib import Path

from modules.vortaro import Vortaro
from modules.gui import GUIApplication
from modules.teksto import Teksto
import tkinter

TESTTEXT = Path(__file__).parent / "input" / "Teksto.txt"

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")
#BAZAVORTARO = Path(__file__).parent.parent.joinpath(config['Paths']['main_dictionary'])
BAZAVORTARO = Path(config['Paths']['main_dictionary'])

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "filename",
        help="Имя файла с текстом для обработки. Должен быть в кодировке Unicode (UTF-8)",
        type=Path,
        default=TESTTEXT,
        nargs="?",  # argument is optional
    )
    parser.add_argument(
        "--gui", help="Запустить графический интерфейс", action="store_true"
    )
    parser.add_argument(
        "--dict",
        help="Имя файла словаря",
        type=Path,
        default=BAZAVORTARO,
        nargs="?",  # argument is optional
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.gui:
        root = tkinter.Tk()
        application = GUIApplication(root, args)
        root.mainloop()
    else:
        try:
            vortaro = Vortaro().elsxuti_el_dosieron(BAZAVORTARO, kamp_num=3)
            texto = Path(args.filename).read_text(encoding="utf-8-sig")
            teksto = Teksto(texto, vortaro)
            teksto.prilabori()
            teksto.write_down()
        except Exception as e:
            print(e)
        else:
            print(f"Словарь сохранен")
