import streamlit as st
import pandas as pd
import joblib

# Load the model
try:
    model = joblib.load("model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None

# Define the valid values for each feature
valid_values = {
    "Intake_Type": ['Stray', 'Public Assist', 'Owner Surrender', 'Abandoned', 'Euthanasia Request'],
    "Intake_Condition": ['Normal', 'Sick', 'Injured', 'Pregnant', 'Nursing', 'Aged', 'Medical', 'Unknown', 'Congenital', 'Other', 'Behavior', 'Neonatal', 'Med Attn', 'Feral'],
    "Animal_Type": ['Dog', 'Cat'],
    "Sex_Upon_Intake": ['Neutered Male', 'Spayed Female', 'Intact Male', 'Intact Female', 'Unknown'],
    "Animal_Group": ['Hound Group', 'Sporting Group', 'Cat', 'Working Group', 'Terrier Group', 'Toy Group', 'Herding Group', 'Non-Sporting Group', 'Other']
}

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
            Intake_Type = st.text_input(label="**Intake Type :**").strip().lower()
            Intake_Condition = st.text_input(label="**Intake Condition :**").strip().lower()
            Animal_Type = st.text_input(label="**Animal Type :**").strip().lower()
            Sex_Upon_Intake = st.text_input(label="**Sex upon Intake :**").strip().lower()
            Age_Upon_Intake_Days = st.number_input(label="**Age in days :**", step=1)
            Animal_Group = st.text_input(label="**Animal Group :**").strip().lower()

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
        missing_fields = [field for field in model_data_dict if not model_data_dict[field]]
        invalid_fields = {field: value for field, value in model_data_dict.items() if field in valid_values and value not in valid_values[field]}

        if missing_fields:
            st.error(f"Please fill out all the fields: {', '.join(missing_fields)}")
        elif invalid_fields:
            for field, value in invalid_fields.items():
                st.error(f"Invalid value for {field}: {value}. Expected values are: {', '.join(valid_values[field])}")
        else:
            try:
                prediction = model.predict(model_data_df)[0]
                prediction_proba = model.predict_proba(model_data_df)[0]
                prediction_percentage = max(prediction_proba) * 100
                st.write(f"Prediction result: {prediction}")
                st.write(f"Prediction confidence: {prediction_percentage:.2f}%")
            except KeyError as e:
                st.error(f"KeyError: {e}")
                st.write(f"Expected columns: {model.named_steps['preprocessor'].transformers_[0][2]}")
                st.write(f"Columns in model_data_df: {model_data_df.columns}")
            except Exception as e:
                st.error(f"Error making prediction: {e}")
                st.text(e)
