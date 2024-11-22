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

    le = LabelEncoder()
    df['Tulemus_kood'] = le.fit_transform(df['Tulemus'])

    df['Koduvõõrsil_kood'] = df['Koduvõõrsil'].map({'Kodu': 1, 'Võõrsil': 0})

    df['Eelmine_kohtumine'] = df['Tulemus_kood'].shift(1)
    df = df.dropna()  

    return df

def loo_ennustusmudel(faili_tee):
    df = töödelda_mängu_andmed(faili_tee)

    X = df[['Koduvõõrsil_kood', 'Eelmine_kohtumine']]  
    y = df['Tulemus_kood']  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mudel = RandomForestClassifier(n_estimators=100, random_state=42)
    mudel.fit(X_train, y_train)

    y_pred = mudel.predict(X_test)

    täpsus = accuracy_score(y_test, y_pred)
    print(f"Täpsus: {täpsus:.2f}")
    print("Täiendavad mõõdikud:")
    print(classification_report(y_test, y_pred, target_names=['Kaotus', 'Viik', 'Võit']))

    return mudel, le

def ennusta_mängu_tulemus(mudel, le, koduvõõrsil, eelmine_tulemus):
    koduvõõrsil_kood = 1 if koduvõrsil == 'Kodu' else 0
    eelmine_tulemus_kood = le.transform([eelmine_tulemus])[0]

    ennustus = mudel.predict([[koduvõrsil_kood, eelmine_tulemus_kood]])
    ennustatud_tulemus = le.inverse_transform(ennustus)[0]
    return ennustatud_tulemus

faili_tee = 'meeskonna_mängud.csv' 
mudel, le = loo_ennustusmudel(faili_tee)

ennustatud_tulemus = ennusta_mängu_tulemus(mudel, le, koduvõõrsil='Kodu', eelmine_tulemus='Võit')
print(f"Järgmise mängu ennustatud tulemus: {ennustatud_tulemus}")
