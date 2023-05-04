import unittest
from unittest import TestCase

from modules.dismorfemigilo import Dismorfemo
from modules.tformatilo import sen_x_igi
from modules.lingvaj_konstantoj import VORTETOJ

class TestClient(TestCase):
    def setUp(self):
        pass
    def test_espsof_base(self):
        gxustaj_disigoj = {}
        with open("./tests/espsof_vortoj.txt", "r") as dosiero:
            linioj = dosiero.readlines()
        for linio in linioj:
            vorto = linio.split('\t')[0]
            gxusta_disigo = sen_x_igi(linio.split('\t')[1].replace("'", "-")[:-1])
            gxustaj_disigoj[vorto] = gxusta_disigo
        vortnum = {}
        erarlinioj = []
        for vorto, gxusta_disigo in gxustaj_disigoj.items():
            disigoj = Dismorfemo(vorto).disigoj
            disignum = len(disigoj)
            #self.assertEqual(disignum, 1) # есть только один хороший разбор
            if not disigoj:
                vortnum[disignum] = vortnum.get(disignum, 0) + 1
                erarlinioj.append(f"{vorto}\t{gxusta_disigo}\t0\t\n")
                continue
            aspekto_de_plejbona_disigo = str(disigoj[0])
            #self.assertEqual(aspekto_de_plejbona_disigo, gxusta_disigo)
            if aspekto_de_plejbona_disigo != gxusta_disigo:
                vortnum[disignum] = vortnum.get(disignum, 0) + 1
                erarlinioj.append(f"{vorto}\t{gxusta_disigo}\t{disignum}\t{aspekto_de_plejbona_disigo}\n")
        with open("./tests/malbonaj_disigoj.txt", "w") as dosiero:
            dosiero.write("\t".join(["vorto", "espsof_disigo", "kvanto_da_disigoj", "malgxusta_disigo\n"]))
            dosiero.writelines(erarlinioj)
        print(vortnum)

if __name__ == '__main__':
    unittest.main()