def consolidar_dictamen(
    criterios_legales: list[dict],
    resultados_legal: list[dict],
    resultados_tecnico: list[dict],
) -> dict:
    obligatorios_incumplidos = [
        r for r, c in zip(resultados_legal, criterios_legales)
        if c["obligatorio"] and r["veredicto"] != "Cumple"
    ]
    habilitado = len(obligatorios_incumplidos) == 0

    cumplidos_tecnicos = sum(1 for r in resultados_tecnico if r["veredicto"] == "Cumple")
    puntaje = round((cumplidos_tecnicos / len(resultados_tecnico)) * 100, 2) if resultados_tecnico else 0.0

    if obligatorios_incumplidos:
        motivos = "; ".join(r["justificacion"] for r in obligatorios_incumplidos)
        justificacion = f"Descalificado por incumplimiento legal: {motivos}"
    else:
        justificacion = "Habilitado legalmente. Puntaje técnico calculado sobre criterios evaluados."

    citas = [c for r in resultados_legal + resultados_tecnico for c in r.get("citas", [])]

    return {
        "veredicto": "Cumple" if habilitado else "No Cumple",
        "habilitado": habilitado,
        "puntaje": puntaje,
        "justificacion": justificacion,
        "citas": citas,
    }
