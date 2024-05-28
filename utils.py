from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)
from sklearn.preprocessing import RobustScaler
from sklearn.compose import ColumnTransformer
import streamlit.components.v1 as components
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit_nested_layout
import streamlit as st
import pandas as pd
import numpy as np
# import mlflow
import hmac
import os


def load_css(file_name="src/styleh.css"):
    with open(file_name) as f:
        css = f"<style>{f.read()}</style>"
    return css


# Layout of the page
def page_layout():
    st.set_page_config(layout="wide")

    css = load_css()
    st.markdown(css, unsafe_allow_html=True)

    st.components.v1.html(
        """
        <script>
        // Modify the decoration on top to reuse as a banner

        // Locate elements
        var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
        var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];

        // Observe sidebar size
        function outputsize() {
            decoration.style.left = `${sidebar.offsetWidth}px`;
        }

        new ResizeObserver(outputsize).observe(sidebar);

        // Adjust sizes
        outputsize();
        decoration.style.height = "5.0rem";
        decoration.style.right = "45px";

        // Adjust image decorations
        decoration.style.backgroundImage = "url(https://i.ibb.co/X7sR5Mj/banner-1.png)";
        decoration.style.backgroundSize = "contain";
        </script>
        """,
        width=0,
        height=0,
    )

    with st.sidebar:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.sidebar.image("src/assets/logo.png", width=125)









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


# reset button to reset the page
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


def header(txt: str, size: int):
    header = st.markdown(
        f"<h{size} style='text-align: center;color: #00286a'> {txt} </h{size}>",
        unsafe_allow_html=True,
    )
    return header


@st.cache_resource
def htmlopen(path: str, h, w):
    HtmlFile = open(path, "r", encoding="utf-8")
    source_code = HtmlFile.read()
    components.html(source_code, height=h, width=w)


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


# plots---------------------------------------------------------------------------------------------------------------------------------------------------------------------
@st.cache_resource
def plot(data, col1, col2, cluster, model_data_indices):
    color_map = {2: "#41cbaa", 1: "#237d92", 0: "#ffe231", 3: "#ffb228"}
    colors = data[cluster].map(color_map)

    fig1, ax1 = plt.subplots(figsize=(5, 5))
    scatter = ax1.scatter(data[col2], data[col1], c=colors, s=50)

    ax1.set_xlabel("Days since last connection", color="black")
    ax1.set_ylabel("Total spent", color="black")

    ax1.tick_params(axis="x", colors="black", direction="out", length=3, width=1)
    ax1.tick_params(axis="y", colors="black", direction="out", length=3, width=1)

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Identify the indices of points from model_data_df
    model_indices = data.index.isin(model_data_indices)

    # Highlight points from model_data_df with a red outline
    scatter.set_edgecolor(["red" if idx else "black" for idx in model_indices])
    scatter.set_linewidth(1)  # Increase the width of the outline for better visibility

    legend_labels = {
        2: "Best Customer",
        1: "High value Customer",
        0: "Potential Customer",
        3: "Low Value Customer",
    }
    custom_legend = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=legend_labels[i],
            markerfacecolor=color,
            markersize=8,
            markeredgewidth=1,
            markeredgecolor="black",
        )
        for i, color in color_map.items()
    ]

    legend = ax1.legend(handles=custom_legend, title="Cluster", loc="upper left")
    plt.setp(legend.get_title(), color="black")
    plt.setp(legend.get_texts(), fontsize=8)

    # ax1.set_facecolor("#00286a")
    st.pyplot(fig1, use_container_width=True)


@st.cache_resource
def pieplot(data, column):
    color_map = {2: "#41cbaa", 1: "#237d92", 0: "#ffe231", 3: "#ffb228"}
    counts = data[column].value_counts()
    colors = [color_map[i] for i in counts.index]
    fig2, ax2 = plt.subplots(figsize=(8, 8))

    label_map = {
        2: "Best Customer",
        1: "High Value Customer",
        0: "Potential Customer",
        3: "Low Value Customer",
    }

    ax2.pie(
        counts,
        labels=[label_map[i] for i in counts.index],
        autopct="%1.1f%%",
        textprops={"color": "#000000", "fontsize": 15},
        colors=colors,
    )
    ax2.set_facecolor("#d7dcd6")
    ax2.set_aspect("equal")
    st.pyplot(fig2)


def radar_processor(data):
    scaler = RobustScaler()
    clus_rfm_mean = data[
        [
            "TOTALPRICE",
            "STATUS_DELETED",
            "STATUS_PENDING",
            "STATUS_VALIDATED",
            "RECENCY",
        ]
    ]
    columns = clus_rfm_mean.columns
    clus_rfm_mean = scaler.fit_transform(clus_rfm_mean)
    clus_rfm_mean = pd.DataFrame(clus_rfm_mean, columns=columns)
    clus_rfm_mean.columns = columns
    clus_rfm_mean = pd.DataFrame(clus_rfm_mean.mean())
    values_mean = clus_rfm_mean[0].values
    ranges = [0.3, 0.45, 0.5, 0.75, 0.1]
    for idx, value in enumerate(ranges):
        values_mean[idx] = values_mean[idx] / ranges[idx]

    return values_mean


def individual_radar(data, radar_name, color):
    categories = [
        "TOTALPRICE",
        "STATUS_DELETED",
        "STATUS_PENDING",
        "STATUS_VALIDATED",
        "RECENCY",
    ]
    categories.append(categories[0])

    data = np.append(data, data[0])

    figr = go.Figure()

    figr.add_trace(
        go.Scatterpolar(r=data, theta=categories, line_color=color, name=radar_name)
    )

    figr.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        width=400,
        height=400,
    )

    figr.update_polars(radialaxis=dict(visible=False, range=[0, 1]))

    st.plotly_chart(figr)


def radar(doto):
    best_cus = radar_processor(doto[doto["CLUSTER"].isin([2])])
    high_cus = radar_processor(doto[doto["CLUSTER"].isin([1])])
    potential_cus = radar_processor(doto[doto["CLUSTER"].isin([0])])
    low_cus = radar_processor(doto[doto["CLUSTER"].isin([3])])

    best_cus = np.append(best_cus, best_cus[0])
    high_cus = np.append(high_cus, high_cus[0])
    potential_cus = np.append(potential_cus, potential_cus[0])
    low_cus = np.append(low_cus, low_cus[0])

    categories = [
        "TOTALPRICE",
        "STATUS_DELETED",
        "STATUS_PENDING",
        "STATUS_VALIDATED",
        "RECENCY",
    ]
    categories.append(categories[0])

    figo = go.Figure()

    figo.add_trace(
        go.Scatterpolar(
            r=best_cus, theta=categories, line_color="#41cbaa", name="Best Customers"
        )
    )

    figo.add_trace(
        go.Scatterpolar(
            r=high_cus,
            theta=categories,
            line_color="#237d92",
            name="High value Customer",
        )
    )

    figo.add_trace(
        go.Scatterpolar(
            r=potential_cus,
            theta=categories,
            line_color="#ffe231",
            name="Potential Customers",
        )
    )

    figo.add_trace(
        go.Scatterpolar(
            r=low_cus,
            theta=categories,
            line_color="#ffb228",
            name="Low Value Customers",
        )
    )

    figo.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        width=400,
        height=400,
    )

    figo.update_polars(radialaxis=dict(visible=False, range=[0, 1]))

    st.plotly_chart(figo)
