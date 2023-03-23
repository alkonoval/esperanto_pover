import unittest
from unittest import TestCase
from modules.dismorfemigilo import Dismorfemo
from modules.dosierojn_ls import x_igi, sen_x_igi
from modules.lingvaj_konstantoj import VORTETOJ

class TestClient(TestCase):
    def setUp(self):
        # слова, которые по разным причинам разбираются некорректно
        self.malbonaj_vortoj = [
            "ĉielo",
            "esperante",
            "georgia"
        ]
    def test_malfacilajn_vortojn(self):
        gxustaj_disigoj = {
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
            "arbetaro" : "arb-et-ar-o",
            "disiradis" : "dis-ir-ad-is",
            "filineton" : "fil-in-et-on",
        }
        for vorto, gxusta_disigo in gxustaj_disigoj.items():
            vorto = x_igi(vorto)
            vdis = Dismorfemo(vorto)
            disigo = sen_x_igi(str(vdis.plejbona_disigo))
            self.assertEqual(disigo, gxusta_disigo)
            self.assertEqual(len(vdis.disigoj), 1) # есть только один хороший разбор
    def test_multsignifajn_vortojn(self):
        """ Протестировать слова, имеющие больше одного корректного разбора
        """
        gxustaj_disigoj = {
            "pikradetoj" : set(["pik-rad-et-oj", "pi-krad-et-oj"]),
        }
        for vorto in gxustaj_disigoj.keys():
            vdis = Dismorfemo(x_igi(vorto))
            disigoj = set(map(lambda x: str(x), vdis.disigoj))
            self.assertEqual(disigoj, gxustaj_disigoj[vorto])

    def test_vortetojn(self):
        for vorto in VORTETOJ.cxiuj:
            vdis = Dismorfemo(vorto)
            self.assertEqual(str(vdis.plejbona_disigo), vorto)

if __name__ == '__main__':
    unittest.main()