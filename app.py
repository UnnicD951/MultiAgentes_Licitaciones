import streamlit as st

from auth import acceso_autorizado
from views import comite, postor

st.set_page_config(page_title="Comité Evaluador Sintético", layout="wide")

st.sidebar.title("Comité Evaluador Sintético")
vista = st.sidebar.radio("Selecciona tu portal", ["Comité / Administrador", "Postor / Participante"])

if vista == "Comité / Administrador":
    if acceso_autorizado():
        comite.render()
else:
    postor.render()
