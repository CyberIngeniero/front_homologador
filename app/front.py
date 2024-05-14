import chardet
import pandas as pd
import streamlit as st

# import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Homologador de Vehículos HDI",
    page_icon="./assets/favicon.png",
    layout="wide",
)

# CSS personalizado para reducir el espacio vertical
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1rem;
    }
    .sidebar .block-container{
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal con logo
st.image("./assets/logo.png", width=150)
st.header("Homologador de Vehículos")
st.subheader("by Modelling Team")

st.markdown("---")

# Encabezado del sidebar con logo
st.sidebar.image("./assets/logo.png", width=150)
st.sidebar.header("Visualization Settings")

# Subir archivo
# agrega espacion vertical
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV or Excel file. (200MB max)",
    type=["csv", "xlsx"],
)


def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    file.seek(0)  # Volver al inicio del archivo después de leer
    return result["encoding"]


if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "csv":
        encoding = detect_encoding(uploaded_file)
        try:
            df = pd.read_csv(uploaded_file, encoding=encoding)
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            df = None
    elif file_type == "xlsx":
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            df = None

    if df is not None:
        df["VALIDATE"] = True

        # Guardar nombres originales de las columnas
        original_columns = df.columns.tolist()

        # Permitir a los usuarios cambiar los nombres de las columnas
        st.sidebar.subheader("Edit Column Names")
        new_column_names = {}
        for col in original_columns:
            new_col_name = st.sidebar.text_input(f"Rename '{col}' to:", col)
            new_column_names[col] = new_col_name

        # Crear una copia del DataFrame con los nuevos nombres de columnas
        renamed_df = df.rename(columns=new_column_names)

        columns_to_display = st.sidebar.multiselect(
            "Select columns to display",
            options=list(renamed_df.columns),
            default=list(renamed_df.columns[:10]),
        )

        # Configurar la edición del dataframe
        edited_df = st.data_editor(
            renamed_df[columns_to_display],
            column_config={
                "VALIDATE": st.column_config.CheckboxColumn(
                    "VALIDATE",
                    help="Select your **validate** rows",
                    default=True,
                )
            },
        )

        # Agregar botón "Procesar!"
        if st.button("Procesar!"):
            st.success("Proceso realizado con éxito!")

else:
    st.write("Please upload a file to the application.")
