import streamlit as st
import pandas as pd
import random
import requests
import joblib
import json
from utils import *

# model = joblib.load("src/assets/model.pkl") #CHANGE TO MODEL PATH

if "reset" not in st.session_state:
    st.session_state["reset"] = False

col1, col2 = st.columns((1, 1), gap="small")

with col1:
    st.markdown("#")
    st.markdown("#")
    with st.container(border=True):
        header("Animal adoption", 3)
        header("Enter the animal's information :", 4)



        col11, col12 = st.columns((1, 1), gap="medium")

        with col11:

            Intake_Type = st.text_input(label="**Intake Type :**")
            Intake_Condition = st.text_input(label="**Intake Condition :**")
            Animal_Type = st.text_input(label="**Animal Type :**")

        with col12:
            Sex_upon_Intake = st.text_input(label="**Sex upon Intake :**")
            Age_Upon_Intake_Days = st.number_input(label="**Age in days :**", step = 1)
            Animal_Group = st.text_input(label="**Animal Group :**")

        model_data_dict = {
            "Intake_Type": Intake_Type,
            "Intake_Condition": Intake_Condition,
            "Animal_Type" : Animal_Type,
            "Sex_upon_Intake": Sex_upon_Intake,
            "Animal_Group": Animal_Group,
            "Age_Upon_Intake_Days": Age_Upon_Intake_Days
        }

        model_data_df = pd.DataFrame(model_data_dict, index=[0])

# Add a button for prediction
if st.button("Get Prediction"):
        if not Intake_Type or not Intake_Condition or not Animal_Type or not Sex_upon_Intake or not Age_Upon_Intake_Days or not Animal_Group :
            st.error("Please fill out all the fields")
        else :
            prediction = random.choice(["Transfer","Adoption","Return to Owner"])
            st.write(f"Prediction result : {prediction}")
