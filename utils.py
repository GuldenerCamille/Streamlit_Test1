import streamlit as st
import pandas as pd
import numpy as np
import joblib

def load_css(file_name="src/styleh.css"):
    with open(file_name) as f:
        css = f"<style>{f.read()}</style>"
    return css

def header(txt: str, size: int):
    header = st.markdown(
        f"<h{size} style='text-align: center;color: #00286a'> {txt} </h{size}>",
        unsafe_allow_html=True,
    )
    return header

def reset_data():
    st.cache_data.clear()
    st.cache_resource.clear()
    for key in st.session_state.keys():
        del st.session_state[key]

def reset_prediction_button(key):
    col111, col112, col113 = st.columns((1.35, 2, 1), gap="small")
    with col112:
        if st.session_state["reset"] == True:
            st.markdown("#")
            if st.button("Make a new prediction", key=key):
                st.session_state["sent"] = "lel"
                st.session_state["reset"] = False
                st.session_state["model_df"] = None
                st.cache_data.clear()
                st.rerun()

def file_info():
    count_file_df_rows = len(st.session_state["upload_file_df"].index)
    st.markdown(
        f"There are **{count_file_df_rows}** rows in your file", unsafe_allow_html=True
    )
    st.dataframe(
        pd.DataFrame(st.session_state["upload_file_df"]),
        use_container_width=True,
        height=450,
    )

def upload(csv_type):
    if "upload_file_df" in st.session_state:
        reset_button()
        file_info()
    else:
        upload_file(csv_type)

def reset_button():
    if st.button("Import another file"):
        reset_data()
        st.rerun()

def upload_file(csv_type):
    file = st.file_uploader(
        "upload",
        type=["csv", "xlsx"],
        accept_multiple_files=False,
        label_visibility="hidden",
    )
    if file:
        try:
            file_df = pd.ExcelFile(file)
            file_df = pd.read_excel(file_df, dtype=str)
        except:
            if csv_type == ",":
                file_df = pd.read_csv(
                    file, encoding="unicode_escape", encoding_errors="strict", sep=","
                )
            elif csv_type == ";":
                file_df = pd.read_csv(
                    file, encoding="unicode_escape", encoding_errors="strict", sep=";"
                )
        st.session_state["upload_file_df"] = file_df
        st.rerun()

def number_input(name, preset, preset_value):
    if preset == "Best Customers":
        return st.number_input(
            label=f"**{name}**",
            step=1,
            value=preset_value[0],
            disabled=st.session_state["reset"],
        )
    elif preset == "High value Customers":
        return st.number_input(
            label=f"**{name}**",
            step=1,
            value=preset_value[1],
            disabled=st.session_state["reset"],
        )
    elif preset == "Potential Customers":
        return st.number_input(
            label=f"**{name}**",
            step=1,
            value=preset_value[2],
            disabled=st.session_state["reset"],
        )
    elif preset == "Low Value Customers":
        return st.number_input(
            label=f"**{name}**",
            step=1,
            value=preset_value[3],
            disabled=st.session_state["reset"],
        )
    elif preset == "None":
        return st.number_input(
            label=f"**{name}**",
            step=1,
            value=None,
            disabled=st.session_state["reset"],
        )
