from io import BytesIO

from pypdf import PdfReader


def extraer_paginas(contenido: bytes) -> list[dict]:
    reader = PdfReader(BytesIO(contenido))
    paginas = []
    for numero, pagina in enumerate(reader.pages, start=1):
        texto = (pagina.extract_text() or "").strip()
        if texto:
            paginas.append({"pagina": numero, "texto": texto})
    return paginas


def dividir_en_fragmentos(paginas: list[dict], max_caracteres: int = 1500) -> list[dict]:
    fragmentos = []
    for pagina in paginas:
        texto = pagina["texto"]
        for inicio in range(0, len(texto), max_caracteres):
            fragmentos.append({
                "pagina": pagina["pagina"],
                "contenido": texto[inicio:inicio + max_caracteres],
            })
    return fragmentos


def texto_completo(paginas: list[dict]) -> str:
    return "\n\n".join(f"[Página {p['pagina']}]\n{p['texto']}" for p in paginas)
