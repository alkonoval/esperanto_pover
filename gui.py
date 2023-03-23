import tkinter
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog, messagebox

from modules.teksto import Teksto


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
        self.text_input.delete(0.1, tkinter.END)
        self.text_input.insert(0.1, text)

    def _paste(self):
        text = self.clipboard_get()
        self.text_input.insert(self.text_input.index(tkinter.INSERT), text)

    def _ek(self):
        text = self.text_input.get(0.1, tkinter.END).strip()
        if not text:
            messagebox.showerror("Error", "Введите текст на эсперанто")
            return

        try:
            teksto = Teksto(teksto=text)
            teksto.prilabori()

            teksto.skribi_dismorfigon(cel_dnomo="Dismorfemo")
            teksto.skribi_dismorfigon(
                cel_dnomo="Dismorfemo_plendetala", plendetala=True
            )

            teksto.vortareto.save(dnomo="Vortareto")

            teksto.skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(
                "Vortaraj_vortoj_rilate_al_origignaj_vortoj.txt"
            )
            if not len(teksto.vortaraj_vortoj):
                messagebox.showerror(
                    title="Ошибка",
                    message="В тексте нет ни одного известного слова на эсперанто!",
                )
                return
        except Exception as exception:
            messagebox.showerror(title="Ошибка", message=f"Ошибка: {exception}")
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
