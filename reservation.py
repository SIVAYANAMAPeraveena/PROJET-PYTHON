import pandas as pd
from csv_interaction import save_user_data_to_csv


def reservation (email,institut,date,heure,detail):
    data = {
        "email":email,
        "institut": institut,
        "date": date,
        "heure": heure,
        "detail": detail,
    }
    save_user_data_to_csv(data,"reservation_data.csv")


def afficher_reservation(email):
    FILE_PATH = "reservation_data.csv"
    COLUMN_NAMES = ["email", "institut", "date", "heure", "soin", "detail"]
    
    df = pd.read_csv(
        FILE_PATH,
        sep=',',
        dtype=str  
    ).fillna('')

    reservations_df = df[df['email'] == email]

    reservations_list = reservations_df.to_dict('records')
    print(reservations_list)
    
    return reservations_list


def delete_reservation(reservation_to_delete):
    df = pd.read_csv("reservation_data.csv", dtype=str).fillna('')
        
    condition = (df['email'] == reservation_to_delete.get('email', '')) & \
                (df['date'] == reservation_to_delete.get('date', '')) & \
                (df['heure'] == reservation_to_delete.get('heure', '')) & \
                (df['soin'] == reservation_to_delete.get('soin', ''))

    if 'institut' in reservation_to_delete:
            condition &= (df['institut'] == reservation_to_delete['institut'])
    
    df_after_delete = df[~condition]
    
    if len(df_after_delete) < len(df):
        df_after_delete.to_csv("reservation_data.csv", index=False)
        return True
    else:
        return False