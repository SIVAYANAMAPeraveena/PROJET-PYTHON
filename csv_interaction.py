import os
import pandas as pd


def save_user_data_to_csv(data , path_csv):
    df = pd.DataFrame([data])
    # Ajout des données sans l'en-tête si le fichier existe déjà
    if os.path.exists(path_csv):
        df.to_csv(path_csv, mode='a', header=False, index=False)
    else:
        df.to_csv(path_csv, index=False)


