import pandas as pd
import os

class MänguAnalüüs:
    def __init__(self, failide_kaust):
        """
        Klass, mis haldab ja laadib meeskonna andmed.
        :param failide_kaust: Kausta tee, kus asuvad CSV failid.
        """
        self.failide_kaust = failide_kaust
        self.andmed = pd.DataFrame()

    def lae_andmed(self):
        """
        Laeb kõik CSV failid kaustast ja ühendab need üheks DataFrame'iks.
        """
        failid = [os.path.join(self.failide_kaust, fail) for fail in os.listdir(self.failide_kaust) if fail.endswith(".csv")]
        andmete_list = []

        for fail in failid:
            try:
                df = pd.read_csv(fail)
                df['Meeskond'] = os.path.splitext(os.path.basename(fail))[0]
                andmete_list.append(df)
            except Exception as viga:
                print(f"Viga faili {fail} lugemisel: {viga}")

        # Ühenda kõik failid üheks DataFrame'iks
        if andmete_list:
            self.andmed = pd.concat(andmete_list, ignore_index=True)
        else:
            print("Ühtegi kehtivat andmefaili ei leitud.")
