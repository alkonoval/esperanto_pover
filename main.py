import configparser
from argparse import ArgumentParser
from pathlib import Path

from modules.vortaro import DBController
from modules.gui import GUIApplication
from modules.teksto import Analizilo
import tkinter

TESTTEXT = Path(__file__).parent / "input" / "Teksto.txt"

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")
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
        database = DBController()
        database.fill_dictionary_from(str(BAZAVORTARO))
        
        texto = Path(args.filename).read_text(encoding="utf-8-sig")
        analizilo = Analizilo(database)
        analizilo.prilabori(texto)
        analizilo.write_down()
        print("Словарь сохранен")
