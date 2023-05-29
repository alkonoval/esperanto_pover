from pathlib import Path
import sqlite3

from .tformatilo import x_igi, sen_x_igi
from .lingvaj_konstantoj import LEKSEMARO, MORFEMARO
from .utils import senfinajxigi

def radikigi(vortara_vorto):
    return senfinajxigi(
        vortara_vorto,
        finajxoj=MORFEMARO.vortaraj_finajxoj,
        esceptoj=MORFEMARO.afiksoj + LEKSEMARO.cxiuj_vortetoj,
    )

class DBController:
    def __init__(self, filename = ":memory:"):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.connection.commit()
    
    def fill_dictionary_from(self, filename, sep = "\t", preprocessing = True):
        """Считать базу данных из текстового файла"""
        table = "eo_ru"
        self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}(
                                word TEXT PRIMARY KEY,
                                root TEXT,
                                description TEXT,
                                comment TEXT
                                ) WITHOUT ROWID""")
        lines = Path(filename).read_text(encoding = "utf-8-sig").splitlines()
        columns_num = 3 # in the file 3 columns: word, description, comment
        for line in lines:
            split = line.strip().split(sep, maxsplit = columns_num - 1)
            if split[0].isspace() or split[0] == '':
                continue
            split = split + ["" for i in range(columns_num - len(split))]
            word, description, comment = split
            if preprocessing:
                word = x_igi(word.lower()) # word
            root = radikigi(word) # root
            self.cursor.execute(
                f"INSERT INTO {table} VALUES (?, ?, ?, ?)",
                (word, root, description, comment)
            )
        self.cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS ind_word ON {table} (word)")
        self.cursor.execute(f"CREATE INDEX IF NOT EXISTS ind_root ON {table} (root)")
        self.connection.commit()
    
    def get_litle_dictionary(self, words):
        result = []
        for word in words:
            self.cursor.execute(
                'SELECT word, description, comment FROM eo_ru WHERE word = ?',
                (word,)
            )
            result += self.cursor.fetchall()
        return result
    
    def get_roots(self):
        self.cursor.execute(
            'SELECT DISTINCT root FROM eo_ru'
        )
        rezult = {x[0] for x in self.cursor.fetchall()}
        return rezult
    
    def get_words_from_root(self, root):
        self.cursor.execute(
            'SELECT word FROM eo_ru WHERE root = ?',
            (root,)
        )
        rezult = [x[0] for x in self.cursor.fetchall()]
        return rezult

    def search(self, word):
        self.cursor.execute(
            """SELECT word, root, description, comment FROM eo_ru
                WHERE word LIKE ?""",
            (f"{word}%",)
        )
        result = self.cursor.fetchall()
        return result

    def __del__(self):
        self.connection.close()

def html(table):
    output = ""
    columns_num = len(table[0])
    cells = '<td style="vertical-align:top;">{}</td>' * columns_num
    pattern = f"<tr>{cells}</tr>\n"
    def italics(string):
        lbracket = string.count("(")
        rbracket = string.count(")")
        if lbracket == rbracket:
            string = string.replace("(", "<i>(").replace(")", "</i>)")
        return string
    for values in table:
        key = f"<b>{values[0]}</b>"
        values = list(map(italics, values[1:]))
        output += pattern.format(key, *values)
    output = f"<table>\n{output}</table>"
    return output

def txt(table, sep = '\t'):
    return '\n'.join([sep.join(line) for line in table])