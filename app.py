import streamlit as st
import pandas as pd
import joblib
from utils import *

# Load the model
model = joblib.load("model.pkl")

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
            Intake Type = st.text_input(label="**Intake Type :**")
            Intake Condition = st.text_input(label="**Intake Condition :**")
            Animal Type = st.text_input(label="**Animal Type :**")

        with col12:
            Sex upon Intake = st.text_input(label="**Sex upon Intake :**")
            Age_Upon_Intake_Days = st.number_input(label="**Age in days :**", step=1)
            Animal_Group = st.text_input(label="**Animal Group :**")

        model_data_dict = {
            "Intake Type": Intake Type,
            "Intake Condition": Intake Condition,
            "Animal Type": Animal Type,
            "Sex upon Intake": Sex upon Intake,
            "Age_Upon_Intake_Days": Age_Upon_Intake_Days,
            "Animal_Group": Animal_Group
        }

        model_data_df = pd.DataFrame(model_data_dict, index=[0])

# Add a button for prediction
if st.button("Get Prediction"):
    if not Intake_Type or not Intake_Condition or not Animal_Type or not Sex_upon_Intake or not Age_Upon_Intake_Days or not Animal_Group:
        st.error("Please fill out all the fields")
    else:
        prediction = model.predict(model_data_df)
        st.write(f"Prediction result : {prediction[0]}")
