"""
Funciones para leer y validar coordenadas de picos.
"""
import os
import sys

def leer_picos(path):
    """
    Lee un TSV de picos y agrupa las coordenadas por factor de transcripción.

    Args:
        path (str): Ruta al TSV (ej. data/union_peaks_file.tsv).
    Returns:
        dict: {tf_name: [(start,end), ...]}.
    Exits:
        1 si el archivo no existe, está mal formateado o hay coordenadas inválidas.
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: No existe el archivo de picos: {path}")

    peaks_by_tf = {}
    with open(path, 'r') as f:
        next(f)  # Salta la cabecera
        for lineno, line in enumerate(f, start=2):
            cols = line.strip().split('\t')
            if len(cols) < 3:
                sys.exit(f"ERROR: Línea {lineno} mal formateada.")

            tf, s, e = cols[0], cols[1], cols[2]
            try:
                start, end = int(float(s)), int(float(e))
            except ValueError:
                sys.exit(f"ERROR: Coordenadas inválidas en línea {lineno}.")

            if start < 0 or end <= start:
                sys.exit(f"ERROR: Coordenadas fuera de rango en línea {lineno}.")

            peaks_by_tf.setdefault(tf, []).append((start, end))

    if not peaks_by_tf:
        sys.exit("ERROR: No se encontraron picos válidos.")

    total = sum(len(v) for v in peaks_by_tf.values())
    print(f"✔ {total} picos cargados para {len(peaks_by_tf)} TF(s)")
    return peaks_by_tf