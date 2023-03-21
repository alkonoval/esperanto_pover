import unittest
from unittest import TestCase
from modules.dismorfemigilo import Dismorfemo
from modules.dosierojn_ls import x_igi

class TestClient(TestCase):
    def setUp(self):
        pass
    def test_1(self):
        vorto = x_igi('supreniranta')
        self.assertTrue(str(Dismorfemo(vorto).plejbona_disigo) == 'supr-en-ir-ant-a')

if __name__ == '__main__':
    unittest.main()