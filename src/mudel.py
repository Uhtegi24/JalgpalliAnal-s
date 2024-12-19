import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def lae_ja_töötle_meeskonna_andmed(faili_tee, meeskonna_nimi):
    df = pd.read_csv(faili_tee)
    df['Meeskond'] = meeskonna_nimi  # Lisame meeskonna nime veeruna

    vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus']
    if not all(veeru in df.columns for veeru in vajalikud_veerud):
        raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")

    df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])

    # Konverteerime 'Skoor' numbriliseks ja käsitleme vead
    df['Skoor'] = pd.to_numeric(df['Skoor'], errors='coerce')

    # Eemaldame read, kus 'Skoor' on puudu või mitte-numbriline
    df = df.dropna(subset=['Skoor'])

    # Tulemuste kodeerimine
    df['Tulemus_kood'] = LabelEncoder().fit_transform(df['Tulemus'])

    # Koduvõõrsil asukoha kodeerimine
    df['Koduvõõrsil_kood'] = df['Koduvõõrsil'].map({'Kodu': 1, 'Võõrsil': 0})

    # Viimaste mängude keskmise skoori arvutamine
    df['Keskmine_skoor'] = df['Skoor'].rolling(window=3).mean().shift(1)
    df['Keskmine_skoor_vastane'] = df.groupby('Vastane')['Skoor'].transform('mean').shift(1)

    df = df.dropna()  # Eemaldame read, kus on puuduvad väärtused pärast arvutusi

    return df

def valmista_kombineeritud_andmed(meeskonnad):
    """
    Töötleb mitme meeskonna andmefailid ja kombineerib need.
    :param meeskonnad: Loend tuplest (failitee, meeskonna_nimi)
    :return: Kombineeritud andmed ja LabelEncoder
    """
    kombineeritud_df = pd.DataFrame()

    for faili_tee, meeskonna_nimi in meeskonnad:
        df = lae_ja_töötle_meeskonna_andmed(faili_tee, meeskonna_nimi)
        kombineeritud_df = pd.concat([kombineeritud_df, df], ignore_index=True)

    # Kodeerime kõik meeskonnanimed ja vastased ühtselt
    kodeerija = LabelEncoder()
    kombineeritud_df['Meeskond_kood'] = kodeerija.fit_transform(kombineeritud_df['Meeskond'])
    kombineeritud_df['Vastane_kood'] = kodeerija.transform(kombineeritud_df['Vastane'])

    return kombineeritud_df, kodeerija

def treeni_mudel(andmed):
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

def ennusta_tulemus(mudel, kodeerija, koduvõõrsil, keskmine_skoor, keskmine_skoor_vastane):
    koduvõõrsil_kood = 1 if koduvõõrsil == 'Kodu' else 0
    sisend_andmed = [[koduvõõrsil_kood, keskmine_skoor, keskmine_skoor_vastane]]

    ennustus = mudel.predict(sisend_andmed)
    ennustatud_tulemus = kodeerija.inverse_transform(ennustus)[0]
    return ennustatud_tulemus
