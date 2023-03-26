import tkinter
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog, messagebox

from modules.teksto import Teksto

OUTPUT_DIR = Path("./output")


class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Style().theme_use("clam")
        self.pack(expand=True, fill=tkinter.BOTH)

        toolbar = ttk.Frame(self)
        toolbar.pack(side=tkinter.TOP, fill=tkinter.X)

        ttk.Button(toolbar, text="Из файла…", command=self._from_file).pack(
            side=tkinter.LEFT
        )

        ttk.Button(toolbar, text="Вставить", command=self._paste).pack(
            side=tkinter.LEFT
        )

        ttk.Button(toolbar, text="Очистить", command=self._clear).pack(
            side=tkinter.LEFT
        )

        ttk.Button(toolbar, text="Обработать", command=self._ek).pack(side=tkinter.LEFT)

        ttk.Button(toolbar, text="Выход", command=self.quit).pack(side=tkinter.LEFT)

        self.text_input = tkinter.Text(self)
        self.text_input.pack(fill=tkinter.BOTH, expand=True)

    def _from_file(self):
        filetypes = [("Text files", "*.txt"), ("All files", "*")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if not filename:
            return
        text = Path(filename).read_text()
        self._clear()
        self.text_input.insert(0.1, text)

    def _paste(self):
        text = self.clipboard_get()
        self.text_input.insert(self.text_input.index(tkinter.INSERT), text)

    def _clear(self):
        self.text_input.delete(0.1, tkinter.END)

    def _ek(self):
        text = self.text_input.get(0.1, tkinter.END).strip()
        if not text:
            messagebox.showerror("Error", "Введите текст на эсперанто")
            return

        try:
            teksto = Teksto(teksto=text)
            teksto.prilabori()

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # lazy directory creation
            teksto.skribi_dismorfigon(dvojo=OUTPUT_DIR / "Dismorfemo")
            teksto.skribi_dismorfigon(
                dvojo=OUTPUT_DIR / "Dismorfemo_plendetala", plendetala=True
            )

            teksto.vortareto.save(dvojo=OUTPUT_DIR / "Vortareto")

            teksto.skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(
                OUTPUT_DIR / "Vortaraj_vortoj_rilate_al_origignaj_vortoj.txt"
            )
            if not len(teksto.vortaraj_vortoj):
                raise ValueError(
                    "В тексте нет ни одного известного слова на эсперанто!"
                )
        except Exception as exception:
            messagebox.showerror(title="Ошибка", message=f"{exception}")
        else:
            message = f"Обработано слов: {len(teksto.vortaraj_vortoj)}"
            messagebox.showinfo(title="OK", message=message)


class Application(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PoshaVortaroEoRu")
        self.main_window = MainWindow(self)
        self.main_window.pack(expand=True)

        # Try to place the window at the center of the screen
        self.eval("tk::PlaceWindow . center")


def main():
    application = Application()
    application.mainloop()


if __name__ == "__main__":
    main()
