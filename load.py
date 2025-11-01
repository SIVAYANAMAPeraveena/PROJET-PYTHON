import streamlit as st
import random
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
def save_user_data_to_csv(new_data):   
    new_data['email'] = st.session_state.user_email 
    
    new_data_df = pd.DataFrame([new_data])
    
    if not os.path.exists("load_user_data_from_csv.csv"):
        new_data_df.to_csv("load_user_data_from_csv.csv", index=False, mode='w')
    else:
        new_data_df.to_csv("load_user_data_from_csv.csv", index=False, mode='a', header=False)