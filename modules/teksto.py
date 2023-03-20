import re

from .dismorfemigilo import Dismorfemo
from .dosierojn_ls import CelDosiero, FontDosiero, x_igi
from .lingvaj_konstantoj import rafini_vorton
from .utils import forigi_ripetojn_konservante_ordon
from .vortaro import BAZA_VORTARO, Vortaro


class Teksto:
    def __init__(self, teksto=""):
        self.teksto = x_igi(teksto)

    def elsxuti_el_dosieron(self, dnomo):
        self.teksto = FontDosiero(dnomo).legi()
        return self

    def prilabori(self):
        self.vortoj = self.spliti_al_vortoj()
        # словарь: слово -> список его разборов
        self.senlimita_dismorfigo = self._dismorfigi()
        self.dismorfigo = self.senlimita_dismorfigo

        self.vortaraj_vortoj_por = self._ricevi_vortarajn_vortojn_por()

        # self.radikoj = self._ricevi_radikojn()
        self.nerekonitaj_vortoj = self._ricevi_nerekonitajn_vortojn()
        self.vortaraj_vortoj = self._ricevi_vortarajn_vortojn()

        self.vortareto = BAZA_VORTARO.subvortaro(
            self.nerekonitaj_vortoj + self.vortaraj_vortoj
        )

    def spliti_al_vortoj(self, ignori_nombrojn=True, cel_dnomo=None):
        """
        Выдать слова, встречающиеся в тексте и записать их в файл cel_dnomo
        (если требуется)
        """
        vortoj = re.findall("[a-z'\d-]+", self.teksto.lower(), flags=re.IGNORECASE)
        rezulto = forigi_ripetojn_konservante_ordon(vortoj)
        if ignori_nombrojn:
            rezulto = list(filter(lambda x: not x.isdigit(), rezulto))
        if cel_dnomo is not None:
            CelDosiero(cel_dnomo, formatilo=x_igi).skribi_vortliston(rezulto)
        return rezulto

    def _ricevi_nerekonitajn_vortojn(self):
        rezulto = [
            vorto
            for vorto in self.dismorfigo.keys()
            if self.dismorfigo[vorto].disigoj == []
        ]
        return forigi_ripetojn_konservante_ordon(rezulto)

    # def _ricevi_radikojn(self):
    # radikoj = []
    # for vorto in self.vortoj:
    # vortradikoj = self.dismorfigo[vorto].radikoj
    # radikoj += vortradikoj
    # return radikoj

    def _ricevi_vortarajn_vortojn_por(self):
        cxefvortoj_el = BAZA_VORTARO.cxefvortoj_el_radiko()
        vortaraj_vortoj_por = {}
        for vorto in self.vortoj:
            vortinternaj_vortetoj = self.dismorfigo[vorto].vortetoj
            vortaraj_vortoj_por_vorto = []
            vortaraj_vortoj_por_vorto += vortinternaj_vortetoj
            vortradikoj = self.dismorfigo[vorto].radikoj
            for radiko in vortradikoj:
                vortaraj_vortoj_por_vorto += cxefvortoj_el[radiko]
            vortaraj_vortoj_por[vorto] = forigi_ripetojn_konservante_ordon(
                vortaraj_vortoj_por_vorto
            )
        return vortaraj_vortoj_por

    def _ricevi_vortarajn_vortojn(self):
        vortaraj_vortoj = []
        for vorto in self.vortoj:
            vortaraj_vortoj += self.vortaraj_vortoj_por[vorto]
        return forigi_ripetojn_konservante_ordon(vortaraj_vortoj)

    def _dismorfigi(self):
        # словарь: слово -> список его разборов
        rezulto = {}
        for vorto in self.vortoj:
            # брать только один разбор
            rezulto[vorto] = Dismorfemo(vorto, maksimuma_nombro_de_disigoj=1)
            # rezulto[vorto] = Dismorfemo(vorto)
        return rezulto

    def skribi_dismorfigon(self, cel_dnomo, plendetala=False):
        if plendetala:
            kore_por_vortaro = {
                vorto: str(vdis.senlimigaj_disigoj)
                for vorto, vdis in self.dismorfigo.items()
            }
        else:
            kore_por_vortaro = {
                vorto: str(vdis) for vorto, vdis in self.dismorfigo.items()
            }
        Vortaro(kore_por_vortaro).save(dnomo=cel_dnomo)

    def skribi_vortarajn_vortojn_rilate_al_originaj_vortoj(self, cel_dnomo):
        linioj = []
        vortaraj_vortoj = []
        for vorto in self.vortoj:
            for vortara_vorto in self.vortaraj_vortoj_por[vorto]:
                if vortara_vorto in vortaraj_vortoj:
                    continue
                else:
                    linioj.append(f"{vorto}\t{vortara_vorto}")
                    vortaraj_vortoj.append(vortara_vorto)
            if vorto in self.nerekonitaj_vortoj:
                linioj.append(f"{vorto}#\t{rafini_vorton(vorto)}")
        CelDosiero(dnomo=cel_dnomo).skribi_liniojn(linioj)
