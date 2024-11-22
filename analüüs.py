import pandas as pd

def töödelda_mängu_andmed(faili_tee):
    df = pd.read_csv(faili_tee)

    vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus']

    if not all(veeru in df.columns for veeru in vajalikud_veerud):
        raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")

    df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])

    df['Koduvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
    df['Võõrvõit'] = df.apply(lambda rida: rida['Tulemus'] == 'Võit' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)
    df['Kodukaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Kodu' else False, axis=1)
    df['Võõrkaotus'] = df.apply(lambda rida: rida['Tulemus'] == 'Kaotus' if rida['Koduvõõrsil'] == 'Võõrsil' else False, axis=1)

    kogumängud = len(df)
    koduvõidud = df['Koduvõit'].sum()
    võõrvõidud = df['Võõrvõit'].sum()
    kodukaotused = df['Kodukaotus'].sum()
    võõrkaotused = df['Võõrkaotus'].sum()

    koduvõidu_suhe = koduvõidud / kogumängud if kogumängud > 0 else 0
    võõrvõidu_suhe = võõrvõidud / kogumängud if kogumängud > 0 else 0
    kodukaotuse_suhe = kodukaotused / kogumängud if kogumängud > 0 else 0
    võõrkaotuse_suhe = võõrkaotused / kogumängud if kogumängud > 0 else 0

    print(f"Kogumängud: {kogumängud}")
    print(f"Koduvõidud: {koduvõidud} ({koduvõidu_suhe:.2f} võidusuhtega)")
    print(f"Võõrvõidud: {võõrvõidud} ({võõrvõidu_suhe:.2f} võidusuhtega)")
    print(f"Kodukaotused: {kodukaotused} ({kodukaotuse_suhe:.2f} kaotusesuhega)")
    print(f"Võõrkaotused: {võõrkaotused} ({võõrkaotuse_suhe:.2f} kaotusesuhega)")

    return df

faili_tee = 'Arsenal_real_last_10_games.csv'  
töödeldud_andmed = töödelda_mängu_andmed(faili_tee)
