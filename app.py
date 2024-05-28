import streamlit as st
import pandas as pd
import joblib

# Load the model
try:
    model = joblib.load("model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None

if model:
    if "reset" not in st.session_state:
        st.session_state["reset"] = False

    col1, col2 = st.columns((1, 1), gap="small")

    with col1:
        st.markdown("#")
        st.markdown("#")
        with st.container(border=True):
            st.header("Animal adoption")
            st.subheader("Enter the animal's information:")

            col11, col12 = st.columns((1, 1), gap="medium")

            # Input fields
            Intake_Type = st.text_input(label="**Intake Type :**")
            Intake_Condition = st.text_input(label="**Intake Condition :**")
            Animal_Type = st.text_input(label="**Animal Type :**")
            Sex_Upon_Intake = st.text_input(label="**Sex upon Intake :**")
            Age_Upon_Intake_Days = st.number_input(label="**Age in days :**", step=1)
            Animal_Group = st.text_input(label="**Animal Group :**")

            model_data_dict = {
                "Intake_Type": Intake_Type,
                "Intake_Condition": Intake_Condition,
                "Animal_Type": Animal_Type,
                "Sex_Upon_Intake": Sex_Upon_Intake,
                "Animal_Group": Animal_Group,
                "Age_Upon_Intake_Days": Age_Upon_Intake_Days
            }

            model_data_df = pd.DataFrame(model_data_dict, index=[0])

    # Add a button for prediction
    if st.button("Get Prediction"):
        if not Intake_Type or not Intake_Condition or not Animal_Type or not Sex_Upon_Intake or not Age_Upon_Intake_Days or not Animal_Group:
            st.error("Please fill out all the fields")
        else:
            try:
                prediction = model.predict(model_data_df)[0]
                st.write(f"Prediction result: {prediction}")
            except KeyError as e:
                st.error(f"KeyError: {e}")
                st.write(f"Expected columns: {model.named_steps['preprocessor'].transformers_[0][2]}")
                st.write(f"Columns in model_data_df: {model_data_df.columns}")
            except Exception as e:
                st.error(f"Error making prediction: {e}")
                st.text(e)
