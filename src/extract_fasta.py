"""
Script para extraer los picos de unión o "Union Peaks" del genoma de E. Coli,
generando UN archivo FASTA por cada TF.

Inputs:
- genoma_ecoli.fna : Genoma de referencia en formato FASTA
- union_peaks_file.tsv : Coordenadas de picos (cols: TF_name, Peak_start, Peak_end)

Output:
- Para cada TF, un archivo FASTA:
    <outdir>/<TF_name>_peaks.fasta
"""

import os
import sys
import argparse

def parse_args():  # ---------------------------------------------------------- Define y procesa los parámetros de entrada del script
    """
    Define y parsea los argumentos de línea de comando.

    Returns:
        argparse.Namespace: Objeto con atributos genome, peaks y outdir.
    """
    parser = argparse.ArgumentParser(
        description="Extrae los picos de unión por TF y genera FASTA separados"
    )
    parser.add_argument(
        '--genome', required=True,
        help="Ruta al FASTA del genoma (ej: genoma_ecoli.fna)"
    )
    parser.add_argument(
        '--peaks', required=True,
        help="TSV con columnas TF_name, Peak_start, Peak_end (ej: union_peaks_file.tsv)"
    )
    parser.add_argument(
        '--outdir', required=True,
        help="Directorio donde se escribirán los FASTA por TF (se crea si no existe)"
    )
    return parser.parse_args()


def cargar_genoma(path):  # --------------------------------------------------- Carga y concatena el genoma completo desde un archivo FASTA.
    """
    Carga y concatena el genoma completo desde un archivo FASTA.

    Args:
        path (str): Ruta al archivo FASTA de genoma.

    Returns:
        str: Secuencia completa del genoma (sin líneas de cabecera).

    Exits:
        1: Si el archivo no existe o la secuencia resultante está vacía.
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: No existe el archivo de genoma: {path}")

    with open(path, 'r') as f:
        genoma = ''.join(
            linea.strip() for linea in f
            if linea.strip() and not linea.startswith('>')
        )

    if not genoma:
        sys.exit("ERROR: El FASTA de genoma está vacío, inténtalo con otro archivo :(")

    print(f"✔ Genoma cargado (longitud: {len(genoma)} bases)")
    return genoma


def leer_picos(path):  # ------------------------------------------------------ Procesamiento del archivo con lñas coordenadas de los picos 
    """
    Procesa un archivo TSV con coordenadas de picos

    Args:
        path (str): Ruta al TSV con picos (TF_name, Peak_start, Peak_end).

    Returns:
        dict: Mapa {nombre_TF: [(start, end), ...]}.

    Exits:
        1: Si el archivo no existe, mal formato o coordenadas inválidas.
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: No existe el archivo de picos: {path}")

    peaks_by_tf = {}
    with open(path, 'r') as f:
        next(f)  # Salta cabecera
        for num_linea, linea in enumerate(f, start=2):
            partes = linea.strip().split('\t')
            if len(partes) < 3:
                sys.exit(f"ERROR: Línea {num_linea} mal formateada (menos de 3 columnas).")

            tf_name = partes[0]
            try:
                start = int(float(partes[1]))
                end = int(float(partes[2]))
            except ValueError:
                sys.exit(f"ERROR: Coordenadas inválidas en línea {num_linea}.")

            # Validación de coordenadas
            if start < 0 or end <= start:
                sys.exit(f"ERROR: Coordenadas fuera de rango o inicio>=fin en línea {num_linea}.")

            peaks_by_tf.setdefault(tf_name, []).append((start, end))

    if not peaks_by_tf:
        sys.exit("ERROR: No se encontraron picos válidos")

    total = sum(len(v) for v in peaks_by_tf.values())
    print(f"✔ {total} picos encontrados para {len(peaks_by_tf)} TF(s)")
    return peaks_by_tf


def extraer_y_guardar(genoma, peaks_by_tf, outdir):  # -------------------------- Extraccion de los picos 
    """
    Extrae fragmentos genómicos según coordenadas y guarda FASTA por TF.

    Args:
        genoma (str): Secuencia completa del genoma.
        peaks_by_tf (dict): Mapa {TF: [(start,end), ...]}.
        outdir (str): Carpeta donde escribir los archivos FASTA.
    """
    # Crear carpeta de salida si no existe
    os.makedirs(outdir, exist_ok=True)

    for tf_name, intervals in peaks_by_tf.items():
        archivo_fasta = os.path.join(outdir, f"{tf_name}_peaks.fasta")
        with open(archivo_fasta, 'w') as out:
            for idx, (start, end) in enumerate(intervals, 1):
                seq = genoma[start:end]
                out.write(f">{tf_name}_pico_{idx}_{start}_{end}\n{seq}\n")
        print(f"  • {len(intervals)} secuencias para {tf_name} → {archivo_fasta}")

    print("\n✔ ¡Archivos FASTA generados para cada TF!")


def main():  # --------------------------------------------------------------- Flujo
    """
    Flujo principal:
      1. Parsear argumentos
      2. Cargar genoma
      3. Leer picos
      4. Extraer y guardar secuencias
    """
    args = parse_args()

    print("\n=== Extracción de Secuencias FASTA por TF :D ===")
    print("Asegúrate de tener tus archivos y la carpeta de salida configurada")

    genoma = cargar_genoma(args.genome)
    peaks_by_tf = leer_picos(args.peaks)
    extraer_y_guardar(genoma, peaks_by_tf, args.outdir)

if __name__ == "__main__":
    main()
