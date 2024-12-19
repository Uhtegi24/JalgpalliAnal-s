import tkinter as tk
from tkinter import filedialog, messagebox
from src.mudel import valmista_kombineeritud_andmed, treeni_ennustusmudel, ennusta_järgmine_mäng
import pandas as pd
from tkinter import simpledialog

# Ülemaailmsed muutujad mudeli ja kodeerija hoidmiseks
globaalne_mudel = None
globaalne_kodeerija = None
globaalne_andmed = None

# Funktsioon andmefailide avamiseks ja kombineerimiseks
def avada_failid():
    """
    Funktsioon kahe meeskonna andmefailide valimiseks ja töötlemiseks.
    """
    fail1 = filedialog.askopenfilename(title="Valige esimese meeskonna andmefail", filetypes=[("CSV Failid", "*.csv")])
    fail2 = filedialog.askopenfilename(title="Valige teise meeskonna andmefail", filetypes=[("CSV Failid", "*.csv")])

    if fail1 and fail2:
        meeskond1 = simpledialog.askstring("Sisend", "Sisestage esimese meeskonna nimi:")
        meeskond2 = simpledialog.askstring("Sisend", "Sisestage teise meeskonna nimi:")
        if meeskond1 and meeskond2:
            try:
                andmed, kodeerija = valmista_kombineeritud_andmed(fail1, fail2, meeskond1, meeskond2)
                global globaalne_andmed, globaalne_kodeerija
                globaalne_andmed = andmed
                globaalne_kodeerija = kodeerija
                messagebox.showinfo("Edu", "Andmed laaditi ja kombineeriti edukalt!")
            except Exception as viga:
                messagebox.showerror("Viga", f"Ilmnes viga andmete töötlemisel: {str(viga)}")
        else:
            messagebox.showwarning("Hoiatus", "Meeskondade nimesid ei määratud.")
    else:
        messagebox.showwarning("Hoiatus", "Andmefaile ei valitud.")

# Funktsioon mudeli treenimiseks
def treeni_mudel():
    """
    Treenib ennustusmudeli kombineeritud andmetel.
    """
    global globaalne_andmed, globaalne_mudel
    if globaalne_andmed is None:
        messagebox.showerror("Viga", "Andmeid pole kombineeritud! Laadige esmalt andmefailid.")
        return
    try:
        mudel = treeni_ennustusmudel(globaalne_andmed)
        globaalne_mudel = mudel
        messagebox.showinfo("Edu", "Ennustusmudel treeniti edukalt!")
    except Exception as e:
        messagebox.showerror("Viga", f"Mudeli treenimisel ilmnes viga: {str(e)}")

# Funktsioon mängu tulemuse ennustamiseks
def ennusta_tulemus():
    """
    Ennustab järgmise mängu tulemuse kasutades treenitud mudelit.
    """
    if globaalne_mudel is None or globaalne_kodeerija is None:
        messagebox.showerror("Viga", "Mudel pole treenitud! Treeni mudel enne ennustamist.")
        return

    koduvõõrsil = filedialog.askstring("Sisend", "Sisestage koduvõõrsil ('Kodu' või 'Võõrsil'):")
    keskmine_skoor = filedialog.askfloat("Sisend", "Sisestage keskmine skoor:")
    keskmine_skoor_vastane = filedialog.askfloat("Sisend", "Sisestage vastase keskmine skoor:")

    if koduvõõrsil and keskmine_skoor is not None and keskmine_skoor_vastane is not None:
        try:
            tulemus = ennusta_järgmine_mäng(
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
root = tk.Tk()
root.title("Jalgpalli meeskonna analüüs ja ennustus")
root.geometry("700x500")

# GUI komponendid
label = tk.Label(root, text="Jalgpalli meeskonna andmete analüüs ja ennustus", font=("Arial", 16))
label.pack(pady=20)

laadi_failid_nupp = tk.Button(root, text="Laadi meeskondade andmefailid", font=("Arial", 12), command=avada_failid)
laadi_failid_nupp.pack(pady=10)

treeni_mudel_nupp = tk.Button(root, text="Treenige ennustusmudel", font=("Arial", 12), command=treeni_mudel)
treeni_mudel_nupp.pack(pady=10)

ennusta_nupp = tk.Button(root, text="Ennusta mängu tulemus", font=("Arial", 12), command=ennusta_tulemus)
ennusta_nupp.pack(pady=10)

# Alusta GUI sündmuste tsüklit
root.mainloop()
