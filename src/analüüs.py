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
        try:
            df = pd.read_csv(faili_tee)
        except Exception as e:
            raise ValueError(f"Viga faili lugemisel: {e}")
        
        # Kontrollime, et kõik vajalikud veerud on olemas
        vajalikud_veerud = ['Kuupäev', 'Koduvõrsil', 'Vastane', 'Skoor', 'Tulemus', 'Vastastele_Väravad', 'Vastastelt_Väravad']
        if not all(veeru in df.columns for veeru in vajalikud_veerud):
            raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")
        
        # Kuupäeva konverteerimine datetime formaati
        df['Kuupäev'] = pd.to_datetime(df['Kuupäev'], errors='coerce')

        # Arvutame koduvõidu, võõrvõidu, kodukaotuse ja võõrkaotuse veerud
        df['Koduvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõrsil'] == 'Kodu' else False, axis=1)
        df['Võõrvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõrsil'] == 'Võõrsil' else False, axis=1)
        df['Kodukaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõrsil'] == 'Kodu' else False, axis=1)
        df['Võõrkaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõrsil'] == 'Võõrsil' else False, axis=1)
        
        # Arvutame väravad, mis meeskond on löönud ja vastased, mis meeskond on löönud
        try:
            df['Koduväravad'] = df.apply(lambda rida: int(rida['Skoor'].split('-')[0]), axis=1)
            df['Võõrväravad'] = df.apply(lambda rida: int(rida['Skoor'].split('-')[1]), axis=1)
        except Exception as e:
            raise ValueError(f"Skoori töötlemise viga: {e}")

        # Arvutame ka vastaste väravad ja vastastelt saadud väravad
        df['Vastaste väravad'] = df['Vastastele_Väravad']
        df['Vastastelt väravad'] = df['Vastastelt_Väravad']
        
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
