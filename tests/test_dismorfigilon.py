import configparser
import unittest
from pathlib import Path
from unittest import TestCase

from modules.vortaro import DBController
from modules.dismorfemigilo import Dismorfemo
from modules.tformatilo import sen_x_igi
from modules.lingvaj_konstantoj import VORTETOJ

config = configparser.ConfigParser()
config.read("config.ini")
BAZAVORTARO = Path(__file__).parent.parent.joinpath(config['Paths']['main_dictionary'])

database = DBController()
database.fill_dictionary_from(str(BAZAVORTARO))
vortaraj_radikoj = database.get_roots()

class TestClient(TestCase):
    def setUp(self):
        # слова, которые по разным причинам разбираются некорректно
        self.malbonaj_vortoj = [
            "ĉielo",
            "esperante",
            "georgia",
            "neniigitaj",
            "cxaro",
            "sovetia"
        ]
    def test_malfacilajn_vortojn(self):
        gxustaj_disigoj = {
            "supreniranta" : "supr-en-ir-ant-a",
            "homamaso" : "hom-amas-o",
            "okulojn" : "okul-ojn",
            "aĉetu" : "aĉet-u",
            "iometon" : "iom-et-on",
            "manĝis" : "manĝ-is",
            "20a" : "20-a",
            "lukto-forkuro" : "lukt-o-for-kur-o",
            "returne" : "re-turn-e",
            "sangopremo" : "sang-o-prem-o",
            "disputis" : "disput-is",
            "20-sekunda" : "20-sekund-a",
            "arbetaro" : "arb-et-ar-o",
            "disiradis" : "dis-ir-ad-is",
            "filineton" : "fil-in-et-on",
            "kuspita" : "kusp-it-a"
        }
        for vorto, gxusta_disigo in gxustaj_disigoj.items():
            disigoj = Dismorfemo(vorto, vortaraj_radikoj).disigoj
            self.assertEqual(len(disigoj), 1) # есть только один хороший разбор
            aspekto_de_plejbona_disigo = str(disigoj[0])
            self.assertEqual(aspekto_de_plejbona_disigo, gxusta_disigo)

    def test_multsignifajn_vortojn(self):
        """ Протестировать слова, имеющие больше одного корректного разбора
        """
        gxustaj_disigoj = {
            "pikradetoj" : set(["pik-rad-et-oj", "pi-krad-et-oj"]),
        }
        for vorto in gxustaj_disigoj.keys():
            disigoj = Dismorfemo(vorto, vortaraj_radikoj).disigoj
            aspekto_por_disigoj = set(map(lambda x: str(x), disigoj))
            self.assertEqual(aspekto_por_disigoj, gxustaj_disigoj[vorto])

    def test_vortetojn(self):
        for vorto in VORTETOJ.cxiuj:
            disigoj = Dismorfemo(vorto, vortaraj_radikoj).disigoj
            self.assertEqual(len(disigoj), 1) # есть только один хороший разбор
            aspekto_de_plejbona_disigo = str(disigoj[0])
            self.assertEqual(aspekto_de_plejbona_disigo, sen_x_igi(vorto))

if __name__ == '__main__':
    unittest.main()