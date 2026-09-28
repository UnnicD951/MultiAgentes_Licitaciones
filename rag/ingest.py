from db.client import get_client
from rag.embeddings import embed_texto
from rag.pdf_extract import dividir_en_fragmentos, extraer_paginas


def indexar_documento(concurso_id: str, postor_id: str | None, origen: str, contenido: bytes) -> int:
    paginas = extraer_paginas(contenido)
    fragmentos = dividir_en_fragmentos(paginas)

    filas = []
    for fragmento in fragmentos:
        embedding = embed_texto(fragmento["contenido"])
        filas.append({
            "concurso_id": concurso_id,
            "postor_id": postor_id,
            "origen": origen,
            "pagina": fragmento["pagina"],
            "contenido": fragmento["contenido"],
            "embedding": embedding,
        })

    if filas:
        get_client().table("documentos_chunks").insert(filas).execute()

    return len(filas)
