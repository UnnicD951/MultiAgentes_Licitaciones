import streamlit as st

from db.client import get_client
from db.storage import subir_archivo
from rag.ingest import indexar_documento


def render():
    st.title("Portal del Postor / Participante")

    client = get_client()
    concursos = client.table("concursos").select("*").eq("estado", "abierto").execute().data

    if not concursos:
        st.info("No hay concursos abiertos en este momento.")
        return

    opciones = {c["id"]: c for c in concursos}
    concurso_id_seleccionado = st.selectbox(
        "Concurso al que postulas",
        list(opciones.keys()),
        format_func=lambda cid: opciones[cid]["nombre"],
    )
    concurso = opciones[concurso_id_seleccionado]
    st.caption(concurso.get("descripcion") or "")

    with st.form("postulacion"):
        ruc = st.text_input("RUC")
        razon_social = st.text_input("Razón Social")
        propuesta_pdf = st.file_uploader("Propuesta Técnica (PDF)", type="pdf")
        cv_pdf = st.file_uploader("CV Documentado (PDF)", type="pdf")
        enviado = st.form_submit_button("Enviar Postulación")

    if not enviado:
        return

    if not ruc or not razon_social or not propuesta_pdf or not cv_pdf:
        st.error("Todos los campos son obligatorios.")
        return

    postor = client.table("postores").insert({
        "concurso_id": concurso["id"],
        "ruc": ruc,
        "razon_social": razon_social,
        "estado": "recibido",
    }).execute().data[0]

    propuesta_bytes = propuesta_pdf.getvalue()
    cv_bytes = cv_pdf.getvalue()

    propuesta_path = f"postores/{postor['id']}/propuesta.pdf"
    cv_path = f"postores/{postor['id']}/cv.pdf"
    subir_archivo(propuesta_path, propuesta_bytes)
    subir_archivo(cv_path, cv_bytes)

    client.table("postores").update({
        "propuesta_pdf_path": propuesta_path,
        "cv_pdf_path": cv_path,
    }).eq("id", postor["id"]).execute()

    try:
        with st.spinner("Indexando tus documentos para la evaluación..."):
            indexar_documento(concurso["id"], postor["id"], "propuesta", propuesta_bytes)
            indexar_documento(concurso["id"], postor["id"], "cv", cv_bytes)
    except Exception:
        st.error(
            "Tu postulación se registró, pero hubo un problema al procesar tus documentos. "
            "Por favor contacta al comité para confirmar que tus archivos se recibieron correctamente."
        )
        return

    st.success("Postulación registrada correctamente. El comité evaluará tu expediente.")
