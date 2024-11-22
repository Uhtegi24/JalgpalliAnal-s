import tkinter as tk
from tkinter import filedialog, messagebox
from analüüs import laadige_andmed
from visualiseerimine import joonista_tulemused
from mudel import treeni_mudel
import pandas as pd

# Funktsioon faili avamiseks ja .txt faili üleslaadimiseks
def avada_fail():
    failitee = filedialog.askopenfilename(
        title="Valige andmefail",
        filetypes=[("Tekstifailid", "*.txt"), ("CSV Failid", "*.csv")]
    )
    
    if failitee:
        try:
            # Laadige andmed valitud failist
            andmed = laadige_andmed(failitee)
            # Kuvage edukas sõnum
            messagebox.showinfo("Edu", f"Andmed laaditi edukalt failist {failitee}")
            
            # Tehke analüüs ja kuvage tulemused
            analüüsi_andmed(andmed)
            # Joonistage tulemused
            joonista_tulemused(andmed)
        except Exception as e:
            # Kui tekib viga, kuvatakse veateade
            messagebox.showerror("Viga", f"Ilmnes viga: {str(e)}")

# Funktsioon andmete analüüsimiseks
def analüüsi_andmed(andmed):
    # Näide analüüsist: Kuvada andmete põhistatistika
    statistika = andmed.describe()
    tulemus_tekst.delete(1.0, tk.END)  # Eemaldage eelmised tulemused
    tulemus_tekst.insert(tk.END, "Andmete analüüsi tulemused:\n")
    tulemus_tekst.insert(tk.END, str(statistika))
    
    # Siia saab lisada ka muid analüüse või trende, nt võitude/kaotuste suhe

# Funktsioon ennustusmudeli treenimiseks (näide)
def ennusta_tulemus():
    failitee = filedialog.askopenfilename(
        title="Valige andmefail ennustusmudeli jaoks",
        filetypes=[("Tekstifailid", "*.txt"), ("CSV Failid", "*.csv")]
    )
    
    if failitee:
        try:
            # Laadige andmed valitud failist
            andmed = laadige_andmed(failitee)
            # Treenige mudel laaditud andmete põhjal
            mudel = treeni_mudel(andmed)
            messagebox.showinfo("Ennustus", "Ennustusmudel treeniti edukalt!")
        except Exception as e:
            # Kui tekib viga, kuvatakse veateade
            messagebox.showerror("Viga", f"Ilmnes viga: {str(e)}")

# Looge peamine aken
root = tk.Tk()
root.title("Jalgpalli meeskonna analüüs")
root.geometry("600x400")

# Lisage juhis, kuidas kasutajat teavitada
label = tk.Label(root, text="Jalgpalli meeskonna mänguandmete analüüs", font=("Arial", 16))
label.pack(pady=20)

# Lisage nupp faili üleslaadimiseks ja andmete analüüsimiseks
laadi_fail_nupp = tk.Button(root, text="Laadi mänguandmete fail", font=("Arial", 12), command=avada_fail)
laadi_fail_nupp.pack(pady=10)

# Lisage nupp ennustusmudeli treenimiseks
ennusta_nupp = tk.Button(root, text="Treenige Ennustusmudel", font=("Arial", 12), command=ennusta_tulemus)
ennusta_nupp.pack(pady=10)

# Lisage tekstiväli, et kuvada analüüsi tulemusi
tulemus_tekst = tk.Text(root, width=70, height=10, wrap=tk.WORD, font=("Arial", 10))
tulemus_tekst.pack(pady=20)

# Alustage GUI sündmuste tsüklit
root.mainloop()
