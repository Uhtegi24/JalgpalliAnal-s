import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def töödelda_mängu_andmed(faili_tee):
    df = pd.read_csv(faili_tee)

    vajalikud_veerud = ['Kuupäev', 'Koduvõõrsil', 'Vastane', 'Skoor', 'Tulemus']
    if not all(veeru in df.columns for veeru in vajalikud_veerud):
        raise ValueError(f"CSV fail peab sisaldama järgmisi veerge: {', '.join(vajalikud_veerud)}")

    df['Kuupäev'] = pd.to_datetime(df['Kuupäev'])

    # Andmete kodeerimine
    le = LabelEncoder()
    df['Tulemus_kood'] = le.fit_transform(df['Tulemus'])

    # Koduvõõrsil asukoha kodeerimine
    df['Koduvõõrsil_kood'] = df['Koduvõrsil'].map({'Kodu': 1, 'Võõrsil': 0})

    # Eelmise mängu tulemuse lisamine
    df['Eelmine_kohtumine'] = df['Tulemus_kood'].shift(1)
    df = df.dropna()  # Eemaldame tühjad read, mis tekivad shift'imise tõttu

    # Kontrollime, kas vajalikud veerud on olemas
    print("Andmed pärast töötlemist:", df.head())
    print("Veerud pärast töötlemist:", df.columns)

    return df, le

def loo_ennustusmudel(faili_tee):
    df, le = töödelda_mängu_andmed(faili_tee)

    # Kontrollime, kas veerud eksisteerivad
    if 'Koduvõrsil_kood' not in df.columns or 'Eelmine_kohtumine' not in df.columns:
        raise ValueError("Puuduvad vajalikud veerud: 'Koduvõrsil_kood' või 'Eelmine_kohtumine'")

    # Andmete jagamine treeninguks ja testimiseks
    X = df[['Koduvõrsil_kood', 'Eelmine_kohtumine']]  # Sõltumatud muutujad
    y = df['Tulemus_kood']  # Sõltuv muutuja (tulemus)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Mudeli loomine ja treenimine
    mudel = RandomForestClassifier(n_estimators=100, random_state=42)
    mudel.fit(X_train, y_train)

    # Ennustamine ja hindamine
    y_pred = mudel.predict(X_test)
    täpsus = accuracy_score(y_test, y_pred)

    print(f"Täpsus: {täpsus:.2f}")
    print("Täiendavad mõõdikud:")
    print(classification_report(y_test, y_pred, target_names=['Kaotus', 'Viik', 'Võit']))

    return mudel, le

def ennusta_mängu_tulemus(mudel, le, koduvõõrsil, eelmine_tulemus):
    # Koodimise jaoks määrame 'Kodu' väärtusele 1, 'Võõrsil' väärtusele 0
    koduvõõrsil_kood = 1 if koduvõõrsil == 'Kodu' else 0
    eelmine_tulemus_kood = le.transform([eelmine_tulemus])[0]  # Kodeeritud eelmine tulemus

    # Ennustamine
    ennustus = mudel.predict([[koduvõõrsil_kood, eelmine_tulemus_kood]])
    ennustatud_tulemus = le.inverse_transform(ennustus)[0]  # Tagasi kodeeritud tulemus
    return ennustatud_tulemus

faili_tee = 'meeskonna_mängud.csv' 
mudel, le = loo_ennustusmudel(faili_tee)

ennustatud_tulemus = ennusta_mängu_tulemus(mudel, le, koduvõõrsil='Kodu', eelmine_tulemus='Võit')
print(f"Järgmise mängu ennustatud tulemus: {ennustatud_tulemus}")
