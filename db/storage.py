from config import STORAGE_BUCKET
from db.client import get_client


def subir_archivo(path: str, contenido: bytes) -> str:
    client = get_client()
    client.storage.from_(STORAGE_BUCKET).upload(
        path,
        contenido,
        {"content-type": "application/pdf", "upsert": "true"},
    )
    return path
