import unittest
from unittest import TestCase
from modules.dismorfemigilo import Dismorfemo
from modules.dosierojn_ls import x_igi, sen_x_igi
from modules.lingvaj_konstantoj import VORTETOJ

class TestClient(TestCase):
    def setUp(self):
        pass
    def test_malfacilajn_vortojn(self):
        self.gxustaj_disigoj = {
            "supreniranta" : "supr-en-ir-ant-a",
            "homamaso" : "hom-amas-o",
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
        }
        for vorto, gxusta_disigo in self.gxustaj_disigoj.items():
            vorto = x_igi(vorto)
            vdis = Dismorfemo(vorto)
            disigo = sen_x_igi(str(vdis.plejbona_disigo))
            self.assertEqual(disigo, gxusta_disigo)
    def test_vortetojn(self):
        for vorto in VORTETOJ.cxiuj:
            vdis = Dismorfemo(vorto)
            self.assertEqual(str(vdis.plejbona_disigo), vorto)

if __name__ == '__main__':
    unittest.main()