import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from src.mudel import valmista_kombineeritud_andmed, treeni_mudel, ennusta_tulemus
from src.visualiseerimine import joonista_tulemused
import pandas as pd
from src.analüüs import MänguAnalüüs
import os

# Globaalmuutujad mudeli ja kodeerija hoidmiseks
globaalne_mudel = None
globaalne_kodeerija = None
globaalne_andmed = None
globaalne_failid = []  # List failide nimede hoidmiseks

# Funktsioon andmefailide avamiseks ja kombineerimiseks
def avada_failid():
    """
    Funktsioon mitme meeskonna andmefailide valimiseks ja töötlemiseks.
    """
    failid = filedialog.askopenfilenames(title="Valige meeskondade andmefailid", filetypes=[("CSV Failid", "*.csv")])

    if len(failid) <= 5:  # Veendu, et valitakse kuni 5 faili
        if failid:
            try:
                # Määrake kausta tee esimesest failist
                failide_kaust = os.path.dirname(failid[0])

                # Loo MänguAnalüüs klassi eksemplar ja laadi andmed
                analüüs = MänguAnalüüs(failide_kaust=failide_kaust)
                globaalne_andmed = analüüs.lae_andmed()  # Laadi andmed

                global globaalne_mudel, globaalne_kodeerija, globaalne_failid
                globaalne_failid = failid  # Salvesta failiteed
                globaalne_andmed = analüüs.andmed  # Kasuta kombineeritud andmeid MänguAnalüüsist

                # Valikumenüü ettevalmistamine failinimedega
                failide_nimed = [os.path.basename(f) for f in failid]  # Ekstrakti ainult failinimed
                valikumenüü['values'] = failide_nimed  # Sea valikumenüü valikud
                valikumenüü.current(0)  # Sea esimene valik vaikimisi valituks

                messagebox.showinfo("Edu", "Kõik andmed laaditi ja kombineeriti edukalt!")
            except Exception as viga:
                messagebox.showerror("Viga", f"Ilmnes viga andmete töötlemisel: {str(viga)}")
        else:
            messagebox.showwarning("Hoiatus", "Andmefaile ei valitud.")
    else:
        messagebox.showwarning("Hoiatus", "Palun valige mitte rohkem kui 5 faili.")

# Funktsioon mängu tulemuste visualiseerimiseks
def visualiseeri_tulemused():
    """
    Funktsioon valitud faili statistika ja graafikute kuvamiseks.
    """
    try:
        valitud_faili_indeks = valikumenüü.current()  # Hangi valitud faili indeks
        if valitud_faili_indeks == -1:
            messagebox.showwarning("Hoiatus", "Valige fail, mille tulemusi visualiseerida.")
            return

        valitud_fail = globaalne_failid[valitud_faili_indeks]
        # Laadi valitud failist andmed
        valitud_andmed = pd.read_csv(valitud_fail)

        # Visualiseeri andmeid funktsiooni joonista_tulemused abil
        joonista_tulemused(valitud_andmed)
    except Exception as e:
        messagebox.showerror("Viga", f"Ilmnes viga graafikute genereerimisel: {str(e)}")

# Funktsioon mudeli treenimiseks
def treeni_ennustusmudel():
    """
    Treenib ennustusmudeli kombineeritud andmetel.
    """
    global globaalne_andmed, globaalne_mudel
    if globaalne_andmed is None:
        messagebox.showerror("Viga", "Andmeid pole kombineeritud! Laadige esmalt andmefailid.")
        return
    try:
        mudel = treeni_mudel(globaalne_andmed)
        globaalne_mudel = mudel
        messagebox.showinfo("Edu", "Ennustusmudel treeniti edukalt!")
    except Exception as e:
        messagebox.showerror("Viga", f"Mudeli treenimisel ilmnes viga: {str(e)}")

# Funktsioon mängu tulemuse ennustamiseks
def ennusta_mängu_tulemus():
    """
    Ennustab järgmise mängu tulemuse kasutades treenitud mudelit.
    """
    if globaalne_mudel is None or globaalne_kodeerija is None:
        messagebox.showerror("Viga", "Mudel pole treenitud! Treeni mudel enne ennustamist.")
        return

    koduvõõrsil = simpledialog.askstring("Sisend", "Sisestage koduvõõrsil ('Kodu' või 'Võõrsil'):")
    keskmine_skoor = simpledialog.askfloat("Sisend", "Sisestage keskmine skoor:")
    keskmine_skoor_vastane = simpledialog.askfloat("Sisend", "Sisestage vastase keskmine skoor:")

    if koduvõõrsil and keskmine_skoor is not None and keskmine_skoor_vastane is not None:
        try:
            # Ennusta tulemus mudeli abil
            tulemus = ennusta_tulemus(
                globaalne_mudel,
                globaalne_kodeerija,
                koduvõõrsil=koduvõõrsil,
                keskmine_skoor=keskmine_skoor,
                keskmine_skoor_vastane=keskmine_skoor_vastane
            )

            messagebox.showinfo("Ennustus", f"Järgmise mängu ennustatud tulemus: {tulemus}")
        except Exception as e:
            messagebox.showerror("Viga", f"Ilmnes viga ennustamisel: {str(e)}")
    else:
        messagebox.showwarning("Hoiatus", "Kõiki sisendväärtusi ei sisestatud.")

# GUI loomine
juur = tk.Tk()
juur.title("Jalgpalli meeskonna analüüs ja ennustus")
juur.geometry("700x500")

# GUI komponendid
silt = tk.Label(juur, text="Jalgpalli meeskonna andmete analüüs ja ennustus", font=("Arial", 16))
silt.pack(pady=20)

laadi_failid_nupp = tk.Button(juur, text="Laadi mitme meeskonna andmefailid", font=("Arial", 12), command=avada_failid)
laadi_failid_nupp.pack(pady=10)

# Valikumenüü faili visualiseerimiseks
valikumenüü_silt = tk.Label(juur, text="Valige fail visualiseerimiseks:", font=("Arial", 12))
valikumenüü_silt.pack(pady=10)

valikumenüü = ttk.Combobox(juur, font=("Arial", 12))
valikumenüü.pack(pady=10)

# Nupp tulemuste visualiseerimiseks
visualiseeri_nupp = tk.Button(juur, text="Visualiseeri tulemused", font=("Arial", 12), command=visualiseeri_tulemused)
visualiseeri_nupp.pack(pady=10)

# Nupp mudeli treenimiseks
treeni_mudel_nupp = tk.Button(juur, text="Treenige ennustusmudel", font=("Arial", 12), command=treeni_ennustusmudel)
treeni_mudel_nupp.pack(pady=10)

# Nupp mängu tulemuse ennustamiseks
ennusta_nupp = tk.Button(juur, text="Ennusta mängu tulemus", font=("Arial", 12), command=ennusta_mängu_tulemus)
ennusta_nupp.pack(pady=10)

# GUI sündmuste tsükli alustamine
juur.mainloop()
