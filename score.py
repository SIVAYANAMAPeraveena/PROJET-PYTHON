import os
import pandas as pd


def put_score(email,score,date):
    print("dedans")
    COLUMNS = ['email', 'score', 'date']
    filename = "score_data.csv"
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        
    if 'date' in df.columns:
        df['date'] = df['date'].astype(str)
    
    new_row = pd.DataFrame([{'email': email, 'score': score, 'date': date}], columns=COLUMNS)

    condition = (df['email'] == email) & (df['date'] == date)
    
    if df[condition].empty:
        df_updated = pd.concat([df, new_row], ignore_index=True)
    else:

        index_to_update = df[condition].index[0]
        
        old_score = df.loc[index_to_update, 'score']
        if score > old_score:
            df.loc[index_to_update, 'score'] = score
            df_updated = df
            print(f"Score mis à jour pour {email} ({old_score} -> {score}).")
        else:
            print(f"Score existant ({old_score}) conservé pour {email} (nouveau score {score} est inférieur ou égal).")
            return True 
    
    df_updated.to_csv(filename, index=False)
    return True


def afficher_score(email):
    FILE_PATH = "score_data.csv"
    COLUMN_NAMES = ["email", "date", "score"]
    
    df = pd.read_csv(
        FILE_PATH,
        sep=',',
        dtype=str 
    ).fillna('')

    score_df = df[df['email'] == email]
    
    score_list = score_df.to_dict('records')
    print(score_list)
    
    return score_list

