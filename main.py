from argparse import ArgumentParser
from pathlib import Path

from modules.gui import GUIApplication
from modules.teksto import Teksto
import tkinter

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
    parser.add_argument(
        "--gui", help="Запустить графический интерфейс", action="store_true"
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
            teksto = Teksto().elsxuti_el_dosieron(dvojo=args.filename)
            teksto.prilabori()
            teksto.write_down()
        except Exception as e:
            print(e)
        else:
            print(f"Словарь сохранен")
