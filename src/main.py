import os
import sys

# Lisame projekti juure tee Python-i otsinguteedesse
def lisa_projekti_juur_otsinguteele():
    """
    Lisab projekti juurkausta Pythoni otsinguteedesse, kui see seal veel pole.
    """
    praegune_kataloog = os.path.dirname(os.path.abspath(__file__))
    projekti_juur = os.path.abspath(os.path.join(praegune_kataloog, ".."))
    if projekti_juur not in sys.path:
        sys.path.insert(0, projekti_juur)

lisa_projekti_juur_otsinguteele()

from src.analüüs import MänguAnalüüs
from src.mudel import treeni_mudel, ennusta_tulemus
from src.GUI import käivita_gui
from src.visualiseerimine import joonista_tulemused


def lae_andmed_ja_analüüsi(kataloog):
    """
    Laeb andmed määratud kaustast ja tagastab analüüsi objekti.
    """
    try:
        analüüs = MänguAnalüüs(kataloog)
        analüüs.lae_kõik_failid()
        return analüüs
    except Exception as viga:
        print(f"Viga andmete laadimisel: {str(viga)}")
        return None


def visualiseeri_meeskonna_andmed(analüüs):
    """
    Visualiseerib valitud meeskonna andmed.
    """
    valitud_meeskond = input("Sisestage meeskond, kelle andmeid soovite visualiseerida: ")
    if valitud_meeskond in analüüs.andmed:
        joonista_tulemused(analüüs.andmed[valitud_meeskond])
    else:
        print(f"Meeskonda {valitud_meeskond} ei leitud.")


def treeni_ja_tee_ennustus(analüüs):
    """
    Treenib mudeli ja teeb mängu tulemuse ennustuse.
    """
    try:
        print("Treeningmudeli loomine...")
        mudel, kodeerija = treeni_mudel(analüüs.andmed)

        print("Mängu tulemuse ennustamine...")
        ennustuse_sisendid = {
            "Koduvõõrsil": input("Sisestage koduvõõrsil ('Kodu' või 'Võõrsil'): "),
            "Eelmine_tulemus": input("Sisestage eelmine tulemus ('Kaotus', 'Viik', 'Võit'): ")
        }
        ennustus = ennusta_tulemus(mudel, kodeerija, ennustuse_sisendid)
        print(f"Ennustatud tulemus: {ennustus}")
    except Exception as viga:
        print(f"Viga mudeli treenimisel või ennustamisel: {str(viga)}")


def põhiprogramm(andmete_kataloog=None, kas_gui=False):
    """
    Peaprogramm, mis koordineerib analüüsi, treeningut, visualiseerimist ja GUI käivitamist.
    """
    andmete_kataloog = andmete_kataloog or input("Sisestage andmefailide kausta tee: ")
    analüüs = lae_andmed_ja_analüüsi(andmete_kataloog)

    if not analüüs:
        print("Andmete laadimine ebaõnnestus. Lõpetan programmi.")
        return

    print("Kuvame meeskondade analüüsi.")
    for meeskond in analüüs.andmed:
        statistika = analüüs.arvuta_statistika(meeskond)
        print(f"Statistika meeskonna {meeskond} kohta:")
        for k, v in statistika.items():
            print(f"  {k}: {v}")

    visualiseeri_meeskonna_andmed(analüüs)
    treeni_ja_tee_ennustus(analüüs)

    if kas_gui:
        print("Käivitame GUI...")
        käivita_gui()


if __name__ == "__main__":
    # Võimaldab GUI prioriteeti, kui kas_gui on True.
    põhiprogramm()
