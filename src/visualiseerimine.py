import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Funktsioon mängu tulemuste visualiseerimiseks
def joonista_tulemused(andmed):
    """
    Joonistab erinevaid graafikuid, et analüüsida jalgpallimeeskonna mängu tulemusi.
    
    :param andmed: pandas DataFrame, mis sisaldab mängude andmeid.
    """
    try:
        # Määrame kõigi graafikute arvu ja paigutuse (2 rida, 2 veergu)
        fig, axs = plt.subplots(2, 2, figsize=(10, 10))
        axs = axs.flatten()  # Ühendada kõik alam-aksid ühte massiivi, et neid hõlpsasti hallata

        # Võitude, kaotuste ja viikide sagedus
        sns.countplot(data=andmed, x='Tulemus', hue='Tulemus', palette='viridis', legend=False, ax=axs[0])
        axs[0].set_title('Võitude, Kaotuste ja Viikide Sagedus')
        axs[0].set_xlabel('Tulemus')
        axs[0].set_ylabel('Mängude Arv')

        # Veendume, et y-teljel on ainult täisarvud
        axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))

        # Kodumängude ja võõrsilmängude tulemused
        sns.countplot(data=andmed, x='Koduvõõrsil', hue='Tulemus', palette='viridis', ax=axs[1])
        axs[1].set_title('Kodumängude ja Võõrsilmängude Tulemused')
        axs[1].set_xlabel('Mängu Asukoht (Kodu/Võõrsil)')
        axs[1].set_ylabel('Mängude Arv')
        axs[1].legend(title='Tulemus')

        # Veendume, et y-teljel on ainult täisarvud
        axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))

        # Mängude arv iga vastase vastu
        sns.countplot(data=andmed, y='Vastane', order=andmed['Vastane'].value_counts().index, palette='viridis', ax=axs[2])
        axs[2].set_title('Mängude Arv Vastaste Kaupa')
        axs[2].set_xlabel('Mängude Arv')
        axs[2].set_ylabel('Vastane')

        # Veendume, et x-teljel on ainult täisarvud
        axs[2].xaxis.set_major_locator(MaxNLocator(integer=True))

        # Võitide, kaotuste ja viikide jaotus igale vastasele
        sns.countplot(data=andmed, y='Vastane', hue='Tulemus', palette='viridis', dodge=True, ax=axs[3])
        axs[3].set_title('Võitide, Kaotuste ja Viikide Jaotus Vastaste Kaupa')
        axs[3].set_xlabel('Mängude Arv')
        axs[3].set_ylabel('Vastane')
        axs[3].legend(title='Tulemus')

        # Veendume, et x-teljel on ainult täisarvud
        axs[3].xaxis.set_major_locator(MaxNLocator(integer=True))

        # Paigutame kõik elemendid ja kuvame
        plt.tight_layout()  # Kohandab graafikute asukohti, et nad ei kattuks
        plt.show()

    except Exception as e:
        print(f"Graafikute loomisel tekkis viga: {str(e)}")
