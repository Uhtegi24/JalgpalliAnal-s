import matplotlib.pyplot as plt
import seaborn as sns

# Funktsioon mängu tulemuste visualiseerimiseks
def joonista_tulemused(andmed):
    """
    Joonistab erinevaid graafikuid, et analüüsida jalgpallimeeskonna mängu tulemusi.
    
    :param andmed: pandas DataFrame, mis sisaldab mängude andmeid.
    """
    try:
        # Võitude, kaotuste ja viikide sagedus
        plt.figure(figsize=(8, 6))
        sns.countplot(data=andmed, x='Tulemus', palette='viridis')
        plt.title('Võitude, Kaotuste ja Viikide Sagedus')
        plt.xlabel('Tulemus')
        plt.ylabel('Mängude Arv')
        plt.show()
        
        # Kodumängude ja võõrsilmängude tulemused
        plt.figure(figsize=(8, 6))
        sns.countplot(data=andmed, x='Asukoht', hue='Tulemus', palette='viridis')
        plt.title('Kodumängude ja Võõrsilmängude Tulemused')
        plt.xlabel('Mängu Asukoht (Kodu/Võõrsil)')
        plt.ylabel('Mängude Arv')
        plt.legend(title='Tulemus')
        plt.show()
        
        # Keskmine väravate arv kodu- ja võõrsilmängudes
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=andmed, x='Asukoht', y='Väravad', palette='viridis')
        plt.title('Väravate Jaotus Kodu- ja Võõrsilmängudes')
        plt.xlabel('Mängu Asukoht')
        plt.ylabel('Väravate Arv')
        plt.show()

        # Mängude arv iga vastase vastu
        plt.figure(figsize=(10, 6))
        sns.countplot(data=andmed, y='Vastane', order=andmed['Vastane'].value_counts().index, palette='viridis')
        plt.title('Mängude Arv Vastaste Kaupa')
        plt.xlabel('Mängude Arv')
        plt.ylabel('Vastane')
        plt.show()
        
    except Exception as e:
        print(f"Graafikute loomisel tekkis viga: {str(e)}")
