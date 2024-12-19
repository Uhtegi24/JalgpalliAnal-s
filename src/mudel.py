import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def lae_ja_töötle_meeskonna_andmed(faili_tee, meeskonna_nimi):
    df = pd.read_csv(faili_tee)
    df = df[df['Meeskond'] == meeskonna_nimi]  # Filtreerime valitud meeskonna andmed

    vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus']
    if not all(veeru in df.columns for veeru in vajalikud_veerud):
        raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")

    df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])

    # Tulemuste kodeerimine
    kodeerija = LabelEncoder()
    df['Tulemus_kood'] = kodeerija.fit_transform(df['Tulemus'])

    # Koduvõõrsil asukoha kodeerimine
    df['Koduvõõrsil_kood'] = df['Koduvõõrsil'].map({'Kodu': 1, 'Võõrsil': 0})

    # Viimaste mängude keskmise skoori arvutamine
    df['Keskmine_skoor'] = df['Skoor'].rolling(window=3).mean().shift(1)
    df['Keskmine_skoor_vastane'] = df.groupby('Vastane')['Skoor'].transform('mean').shift(1)

    df = df.dropna()  # Eemaldame read, kus on puuduvad väärtused

    return df, kodeerija

def valmista_kombineeritud_andmed(meeskond1_fail, meeskond2_fail, meeskond1_nimi, meeskond2_nimi):
    meeskond1_andmed, kodeerija1 = lae_ja_töötle_meeskonna_andmed(meeskond1_fail, meeskond1_nimi)
    meeskond2_andmed, kodeerija2 = lae_ja_töötle_meeskonna_andmed(meeskond2_fail, meeskond2_nimi)

    kombineeritud_df = pd.concat([meeskond1_andmed, meeskond2_andmed], ignore_index=True)

    return kombineeritud_df, kodeerija1  # Eeldame, et mõlemad meeskonnad kasutavad sama kodeerijat

def treeni_ennustusmudel(andmed):
    tunnused = ['Koduvõõrsil_kood', 'Keskmine_skoor', 'Keskmine_skoor_vastane']
    sihtmärk = 'Tulemus_kood'

    X = andmed[tunnused]
    y = andmed[sihtmärk]

    X_treeni, X_testi, y_treeni, y_testi = train_test_split(X, y, test_size=0.2, random_state=42)

    mudel = RandomForestClassifier(n_estimators=100, random_state=42)
    mudel.fit(X_treeni, y_treeni)

    y_ennustused = mudel.predict(X_testi)
    täpsus = accuracy_score(y_testi, y_ennustused)

    print(f"Mudeli täpsus: {täpsus:.2f}")
    print("Klassifitseerimisaruanne:")
    print(classification_report(y_testi, y_ennustused))

    return mudel

def ennusta_järgmine_mäng(mudel, kodeerija, koduvõõrsil, keskmine_skoor, keskmine_skoor_vastane):
    koduvõõrsil_kood = 1 if koduvõõrsil == 'Kodu' else 0
    sisend_andmed = [[koduvõõrsil_kood, keskmine_skoor, keskmine_skoor_vastane]]

    ennustus = mudel.predict(sisend_andmed)
    ennustatud_tulemus = kodeerija.inverse_transform(ennustus)[0]
    return ennustatud_tulemus


