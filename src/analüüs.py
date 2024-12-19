import pandas as pd

def töödelda_mängu_andmed(faili_tee):
    # Lae CSV fail andmetega
    df = pd.read_csv(faili_tee)

    # Uued vajalikud veerud CSV failis
    vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus', 'Vastastele_Löögid', 'Vastastelt_Löögid']

    # Kontrolli, kas kõik vajalikud veerud on olemas
    if not all(veeru in df.columns for veeru in vajalikud_veerud):
        raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")

    # Veendu, et 'Kuupäev' veerg on kuupäeva formaadis
    df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])

    # Lisa veerud mängu tulemuse määramiseks (Kas koduvõit, võõrvõit jne)
    df['Koduvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
    df['Võõrvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)
    df['Kodukaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
    df['Võõrkaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)

    # Arvuta kogumängud ja võidud/kaotused kodus ja võõrsil
    kogumängud = len(df)
    koduvõidud = df['Koduvõit'].sum()
    võõrvõidud = df['Võõrvõit'].sum()
    kodukaotused = df['Kodukaotus'].sum()
    võõrkaotused = df['Võõrkaotus'].sum()

    # Arvuta võiduseisu suhted
    koduvõidu_suhe = koduvõidud / kogumängud if kogumängud > 0 else 0
    võõrvõidu_suhe = võõrvõidud / kogumängud if kogumängud > 0 else 0
    kodukaotuse_suhe = kodukaotused / kogumängud if kogumängud > 0 else 0
    võõrkaotuse_suhe = võõrkaotused / kogumängud if kogumängud > 0 else 0

    # Prindi tulemused
    print(f"Kogumängud: {kogumängud}")
    print(f"Koduvõidud: {koduvõidud} ({koduvõidu_suhe:.2f} võidusuhtega)")
    print(f"Võõrvõidud: {võõrvõidud} ({võõrvõidu_suhe:.2f} võidusuhtega)")
    print(f"Kodukaotused: {kodukaotused} ({kodukaotuse_suhe:.2f} kaotusesuhega)")
    print(f"Võõrkaotused: {võõrkaotused} ({võõrkaotuse_suhe:.2f} kaotusesuhega)")

    # Tagasta töödeldud andmed (DataFrame)
    return df


