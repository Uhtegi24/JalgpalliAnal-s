import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from src.mudel import valmista_kombineeritud_andmed, treeni_mudel, ennusta_tulemus
from src.visualiseerimine import joonista_tulemused
import pandas as pd
from src.analüüs import MänguAnalüüs
import os


# Ìldmaailmsed muutujad mudeli ja kodeerija hoidmiseks
globaalne_mudel = None
globaalne_kodeerija = None
globaalne_andmed = None
globaalne_failid = []  # List to store file names

# Funktsioon andmefailide avamiseks ja kombineerimiseks
def avada_failid():
    """
    Funktsioon mitme meeskonna andmefailide valimiseks ja töötlemiseks.
    """
    failid = filedialog.askopenfilenames(title="Valige meeskondade andmefailid", filetypes=[("CSV Failid", "*.csv")])

    if len(failid) <= 5:  # Ensuring no more than 5 files are selected
        if failid:
            try:
                # Determine the folder path from the first selected file
                failide_kaust = os.path.dirname(failid[0])

                # Create an instance of MänguAnalüüs class and load the data
                analüüs = MänguAnalüüs(failide_kaust=failide_kaust)
                globaalne_andmed = analüüs.lae_andmed()  # Load the data

                global globaalne_mudel, globaalne_kodeerija, globaalne_failid
                globaalne_failid = failid  # Store the file paths
                globaalne_andmed = analüüs.andmed  # Use the combined data from MänguAnalüüs

                # Preparing the dropdown with file names
                failide_nimed = [os.path.basename(f) for f in failid]  # Extract file names only
                dropdown['values'] = failide_nimed  # Set dropdown options
                dropdown.current(0)  # Set the first option as selected by default

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
        selected_file_index = dropdown.current()  # Get selected file index
        if selected_file_index == -1:
            messagebox.showwarning("Hoiatus", "Valige fail, mille tulemusi visualiseerida.")
            return

        selected_file = globaalne_failid[selected_file_index]
        # Load the selected data
        selected_data = pd.read_csv(selected_file)

        # Visualize the data using the function from visualiseerimine.py
        joonista_tulemused(selected_data)
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
def ennusta_tulemus():
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
            # Predict outcome using the model
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
root = tk.Tk()
root.title("Jalgpalli meeskonna analüüs ja ennustus")
root.geometry("700x500")

# GUI komponendid
label = tk.Label(root, text="Jalgpalli meeskonna andmete analüüs ja ennustus", font=("Arial", 16))
label.pack(pady=20)

laadi_failid_nupp = tk.Button(root, text="Laadi mitme meeskonna andmefailid", font=("Arial", 12), command=avada_failid)
laadi_failid_nupp.pack(pady=10)

# Dropdown for selecting file to visualize
dropdown_label = tk.Label(root, text="Valige fail visualiseerimiseks:", font=("Arial", 12))
dropdown_label.pack(pady=10)

dropdown = ttk.Combobox(root, font=("Arial", 12))
dropdown.pack(pady=10)

# Button to visualize results
visualiseeri_nupp = tk.Button(root, text="Visualiseeri tulemused", font=("Arial", 12), command=visualiseeri_tulemused)
visualiseeri_nupp.pack(pady=10)

# Button for training the model
treeni_mudel_nupp = tk.Button(root, text="Treenige ennustusmudel", font=("Arial", 12), command=treeni_ennustusmudel)
treeni_mudel_nupp.pack(pady=10)

# Button for predicting the result
ennusta_nupp = tk.Button(root, text="Ennusta mängu tulemus", font=("Arial", 12), command=ennusta_tulemus)
ennusta_nupp.pack(pady=10)

# Alusta GUI sündmuste tsükill
root.mainloop()