import pandas as pd
import os

class MänguAnalüüs:
    def __init__(self, failide_kaust):
        """
        Klass, mis haldab ja analüüsib mitme meeskonna mängude andmeid.
        :param failide_kaust: Str, kausta tee, kus asuvad meeskondade CSV failid
        """
        self.failide_kaust = failide_kaust
        self.andmed = {}  # Sõnastik meeskondade andmetest
        self.kombineeritud_andmed = None  # Kõigi meeskondade ühendatud DataFrame

    def lae_kõik_failid(self):
        """
        Laeb kõik CSV failid antud kaustast ja hoiab need meeskonna nime järgi.
        """
        andmed_list = []
        for fail in os.listdir(self.failide_kaust):
            if fail.endswith(".csv"):
                meeskond = os.path.splitext(fail)[0]
                faili_tee = os.path.join(self.failide_kaust, fail)
                df = self.töödelda_mängu_andmed(faili_tee)
                df['Meeskond'] = meeskond  # Lisame meeskonna nime veeru
                self.andmed[meeskond] = df
                andmed_list.append(df)
        
        # Kombineerime kõik DataFrame'id üheks, kui on olemas vähemalt üks fail
        if andmed_list:
            self.kombineeritud_andmed = pd.concat(andmed_list, ignore_index=True)

    def töödelda_mängu_andmed(self, faili_tee):
        """
        Töötleb CSV faili andmeid, lisades tuletatud veerud.
        :param faili_tee: Str, CSV faili tee
        :return: Pandas DataFrame, töödeldud andmed
        """
        df = pd.read_csv(faili_tee)
        vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus']
        if not all(veeru in df.columns for veeru in vajalikud_veerud):
            raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")
        df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])
        df['Koduvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
        df['Võõrvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)
        df['Kodukaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
        df['Võõrkaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)
        return df

    def arvuta_statistika(self, meeskond):
        """
        Arvutab statistika konkreetse meeskonna andmete põhjal.
        :param meeskond: Str, meeskonna nimi
        :return: Sõnastik statistiliste näitajatega
        """
        if meeskond not in self.andmed:
            raise ValueError(f"Meeskonna {meeskond} andmeid ei leitud.")
        
        df = self.andmed[meeskond]
        return self._arvuta_statistika_df(df)

    def arvuta_kõigi_statistika(self):
        """
        Arvutab statistika kõigi kombineeritud andmete põhjal.
        :return: Sõnastik statistiliste näitajatega
        """
        if self.kombineeritud_andmed is None:
            raise ValueError("Kombineeritud andmeid ei leitud. Laadige andmed esmalt.")
        
        return self._arvuta_statistika_df(self.kombineeritud_andmed)

    def _arvuta_statistika_df(self, df):
        """
        Abimeetod statistika arvutamiseks.
        :param df: Pandas DataFrame
        :return: Sõnastik statistiliste näitajatega
        """
        kogumängud = len(df)
        koduvõidud = df['Koduvõit'].sum()
        võõrvõidud = df['Võõrvõit'].sum()
        kodukaotused = df['Kodukaotus'].sum()
        võõrkaotused = df['Võõrkaotus'].sum()

        statistika = {
            "Kogumängud": kogumängud,
            "Koduvõidud": koduvõidud,
            "Võõrvõidud": võõrvõidud,
            "Kodukaotused": kodukaotused,
            "Võõrkaotused": võõrkaotused,
            "Koduvõidu suhe": koduvõidud / kogumängud if kogumängud > 0 else 0,
            "Võõrvõidu suhe": võõrvõidud / kogumängud if kogumängud > 0 else 0,
            "Kodukaotuse suhe": kodukaotused / kogumängud if kogumängud > 0 else 0,
            "Võõrkaotuse suhe": võõrkaotused / kogumängud if kogumängud > 0 else 0,
        }

        return statistika   