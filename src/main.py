import os
import sys

# Lisa projekti juurkataloog Pythoni otsinguteedesse
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Impordi moodulid
from src.analüüs import MänguAnalüüs
from src.mudel import treeni_mudel, ennusta_tulemus
from src.GUI import käivita_gui
from src.visualiseerimine import joonista_tulemused


def põhiprogramm():
    """
    Põhiprogramm, mis koordineerib analüüsi, mudeli treenimise, visualiseerimise ja GUI käivitamist.
    """
    # Kausta tee, kus asuvad andmefailid
    failide_kaust = input("Sisestage andmefailide kausta tee: ")

    # Loo analüüsi objekt ja lae andmed
    analüüs = MänguAnalüüs(failide_kaust)
    analüüs.lae_kõik_failid()

    # Kuvame meeskondade andmete analüüsi
    for meeskond in analüüs.andmed:
        print(f"Statistika meeskonna {meeskond} kohta:")
        statistika = analüüs.arvuta_statistika(meeskond)
        for k, v in statistika.items():
            print(f"  {k}: {v}")

    # Visualiseeri ühte meeskonna andmeid
    valitud_meeskond = input("Sisestage meeskond, kelle andmeid soovite visualiseerida: ")
    if valitud_meeskond in analüüs.andmed:
        joonista_tulemused(analüüs.andmed[valitud_meeskond])
    else:
        print(f"Meeskonda {valitud_meeskond} ei leitud.")

    # Treeni mudel ja tee ennustusi
    print("Treeningmudeli loomine...")
    mudel, kodeerija = treeni_mudel(analüüs.andmed)

    print("Mängu tulemuse ennustamine...")
    ennustuse_sisendid = {
        "Koduvõõrsil": input("Sisestage koduvõõrsil ('Kodu' või 'Võõrsil'): "),
        "Eelmine_tulemus": input("Sisestage eelmine tulemus ('Kaotus', 'Viik', 'Võit'): ")
    }
    ennustus = ennusta_tulemus(mudel, kodeerija, ennustuse_sisendid)
    print(f"Ennustatud tulemus: {ennustus}")

    # Käivita GUI, kui see on vajalik
    käivita_gui()


if __name__ == "__main__":
    põhiprogramm()
