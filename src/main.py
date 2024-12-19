import tkinter as tk
from tkinter import filedialog, messagebox
from src.analüüs import töödelda_mängu_andmed  # Andmete töötlemine
from src.visualiseerimine import joonista_tulemused  # Graafikute loomine
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
from src.GUI import luua_gui

luua_gui()


# Ülemaailmsed muutujad mudeli ja kodeerija hoidmiseks
globaalne_mudel = None
globaalne_le = None

# Funktsioon andmefaili avamiseks ja töötlemiseks
def avada_fail():
    """
    Funktsioon andmefaili valimiseks, analüüsimiseks ja visualiseerimiseks.
    """
    failitee = filedialog.askopenfilename(
        title="Valige andmefail",
        filetypes=[("CSV Failid", "*.csv"), ("Tekstifailid", "*.txt")]
    )
    if failitee:
        try:
            # Laadige ja töödelge andmed
            andmed = töödelda_mängu_andmed(failitee)
            messagebox.showinfo("Edu", f"Andmed laaditi ja töödeldi edukalt: {failitee}")
            
            # Kuvage analüüsi tulemused tekstikastis
            analüüsi_andmed(andmed)
            
            # Looge visualisatsioonid
            joonista_tulemused(andmed)
        except Exception as e:
            messagebox.showerror("Viga", f"Ilmnes viga: {str(e)}")

# Funktsioon andmete analüüsimiseks ja tulemuste kuvamiseks
def analüüsi_andmed(andmed):
    """
    Kuvab põhiandmete analüüsi tekstiväljal.
    """
    statistika = andmed.describe()
    tulemus_tekst.delete(1.0, tk.END)
    tulemus_tekst.insert(tk.END, "Andmete analüüsi tulemused:\n")
    tulemus_tekst.insert(tk.END, str(statistika))

# Funktsioon ennustusmudeli treenimiseks
def treeni_mudel():
    """
    Loob ennustusmudeli ja kuvab selle täpsuse.
    """
    failitee = filedialog.askopenfilename(
        title="Valige andmefail mudeli treenimiseks",
        filetypes=[("CSV Failid", "*.csv")]
    )
    if failitee:
        try:
            df = töödelda_mängu_andmed(failitee)
            
            # Andmete ettevalmistus mudeli treenimiseks
            X = df[['Koduvõõrsil_kood', 'Eelmine_kohtumine']]
            y = df['Tulemus_kood']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            mudel = RandomForestClassifier(n_estimators=100, random_state=42)
            mudel.fit(X_train, y_train)
            
            y_pred = mudel.predict(X_test)
            täpsus = accuracy_score(y_test, y_pred)
            raport = classification_report(y_test, y_pred, target_names=['Kaotus', 'Viik', 'Võit'])
            
            # Salvestage mudel ja kodeerija globaalsetesse muutujatesse
            global globaalne_mudel, globaalne_le
            globaalne_mudel = mudel
            globaalne_le = LabelEncoder()
            globaalne_le.fit(df['Tulemus'])
            
            # Kuvage tulemused
            tulemus_tekst.delete(1.0, tk.END)
            tulemus_tekst.insert(tk.END, f"Mudel treenitud edukalt!\n\nTäpsus: {täpsus:.2f}\n")
            tulemus_tekst.insert(tk.END, "Mõõdikud:\n")
            tulemus_tekst.insert(tk.END, raport)
        except Exception as e:
            messagebox.showerror("Viga", f"Ilmnes viga mudeli treenimisel: {str(e)}")

# Funktsioon mängu tulemuse ennustamiseks
def ennusta_tulemus():
    """
    Ennustab järgmise mängu tulemuse, kui mudel on treenitud.
    """
    if globaalne_mudel is None or globaalne_le is None:
        messagebox.showerror("Viga", "Mudel pole treenitud! Treeni mudel enne ennustamist.")
        return
    
    # Küsige sisendväärtused
    koduvõõrsil = filedialog.askstring("Sisend", "Sisestage koduvõõrsil ('Kodu' või 'Võõrsil'):")
    eelmine_tulemus = filedialog.askstring("Sisend", "Sisestage eelmine tulemus ('Kaotus', 'Viik' või 'Võit'):")

    try:
        koduvõõrsil_kood = 1 if koduvõõrsil == 'Kodu' else 0
        eelmine_tulemus_kood = globaalne_le.transform([eelmine_tulemus])[0]
        ennustus = globaalne_mudel.predict([[koduvõõrsil_kood, eelmine_tulemus_kood]])
        ennustatud_tulemus = globaalne_le.inverse_transform(ennustus)[0]
        messagebox.showinfo("Ennustus", f"Järgmise mängu ennustatud tulemus: {ennustatud_tulemus}")
    except Exception as e:
        messagebox.showerror("Viga", f"Ilmnes viga ennustamisel: {str(e)}")

# Looge peamine GUI aken
root = tk.Tk()
root.title("Jalgpalli meeskonna analüüs ja ennustus")
root.geometry("700x500")

# GUI komponendid
label = tk.Label(root, text="Jalgpalli meeskonna andmete analüüs", font=("Arial", 16))
label.pack(pady=20)

laadi_fail_nupp = tk.Button(root, text="Laadi andmefail analüüsiks", font=("Arial", 12), command=avada_fail)
laadi_fail_nupp.pack(pady=10)

treeni_nupp = tk.Button(root, text="Treenige ennustusmudel", font=("Arial", 12), command=treeni_mudel)
treeni_nupp.pack(pady=10)

ennusta_nupp = tk.Button(root, text="Ennusta mängu tulemus", font=("Arial", 12), command=ennusta_tulemus)
ennusta_nupp.pack(pady=10)

tulemus_tekst = tk.Text(root, width=80, height=15, wrap=tk.WORD, font=("Arial", 10))
tulemus_tekst.pack(pady=20)

# Alusta GUI sündmuste tsüklit
root.mainloop()
