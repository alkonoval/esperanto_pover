import tkinter
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog, messagebox

from modules.teksto import Teksto
from modules.vortaro import Vortaro


class MainWindow(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Style().theme_use("clam")
        self.pack(expand=True, fill="both")

        toolbar = ttk.Frame(self)
        ttk.Button(toolbar, text="Из файла…", command=self._from_file).pack(side="left")
        ttk.Button(toolbar, text="Вставить", command=self._paste).pack(side="left")
        ttk.Button(toolbar, text="Очистить", command=self._clear).pack(side="left")
        ttk.Button(toolbar, text="Обработать", command=self._ek).pack(side="left")
        ttk.Button(toolbar, text="Выход", command=quit).pack(side="left")
        toolbar.pack(side="top", fill="x")

        self.text_input = tkinter.Text(self)
        self.text_input.pack(fill="both", expand=True)

    def _from_file(self):
        filetypes = [("Text files", "*.txt"), ("All files", "*")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self._load_file(filename)

    def _load_file(self, filename):
        try:
            text = Path(filename).read_text(encoding="utf-8-sig")
        except (UnicodeDecodeError, FileNotFoundError) as e:
            messagebox.showerror("Ошибка", message=f"Не удалось открыть файл:\n\n{e}")
        else:
            self._clear()
            self.text_input.insert(0.1, text)
    
    def _load_dict(self, dictname):
        try:
            main_dictionary = Vortaro().elsxuti_el_dosieron(dictname, kamp_num=3)
        except (UnicodeDecodeError, FileNotFoundError) as e:
            messagebox.showerror("Ошибка", message=f"Не удалось открыть файл:\n\n{e}")
        else:
            self.main_dictionary = main_dictionary

    def _paste(self):
        text = self.clipboard_get()
        self.text_input.insert(self.text_input.index("insert"), text)

    def _clear(self):
        self.text_input.delete(0.1, "end")

    def _ek(self):
        text = self.text_input.get(0.1, "end").strip()

        try:
            teksto = Teksto(text, self.main_dictionary)
            teksto.prilabori()
            if len(teksto.vortaraj_vortoj):
                teksto.write_down()
            else:
                raise ValueError(
                    "В тексте нет ни одного известного слова на эсперанто!"
                )
        except Exception as exception:
            messagebox.showerror(title="Ошибка", message=f"{exception}")
        else:
            message = f"Обработано слов: {len(teksto.vortaraj_vortoj)}"
            messagebox.showinfo(title="OK", message=message)


class GUIApplication:
    def __init__(self, master, args):
        self.args = args

        self.master = master
        self.master.title("PoshaVortaroEoRu")

        self.main_window = MainWindow(master)
        self.main_window.pack(expand=True)

        # Try to place the window at the center of the screen
        self.master.eval("tk::PlaceWindow . center")

        if self.args:
            self.main_window._load_file(args.filename)
        self.main_window._load_dict(args.dict)
