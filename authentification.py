import streamlit as st
from csv_interaction import * 
import pandas as pd
import os

def sign_up(email, password, username):
    COLUMN_NAMES = ["email", "password", "username"] 

    if os.path.exists("user_data.csv") and os.path.getsize("user_data.csv") > 0:
        df = pd.read_csv("user_data.csv", header=None, names=COLUMN_NAMES).fillna('')
        
        accounts_df = df[df['email'] == email] 
    
        if accounts_df.empty:
            data = {
                "email": email,
                "password": password,
                "username": username,
            }
            save_user_data_to_csv(data, "user_data.csv")
            return 0
    else:
        data = {
            "email": email,
            "password": password,
            "username": username,
        }
        save_user_data_to_csv(data, "user_data.csv")
        return 0 
    
    return 1

def login(email,password):
    df = pd.read_csv("user_data.csv",sep=',', dtype={'password': str}).fillna('')
    accounts_df = df[df['email'] == email]
    
    print(accounts_df)
    if not accounts_df.empty:
        user_row = accounts_df.iloc[0]
        if user_row['password'] == password:
            print("sa match")
            st.session_state.email =  user_row['email']
            st.session_state.prenom =  user_row['username']
            return 0
        
    return 1
