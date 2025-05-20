"""
Funciones para cargar y validar el genoma de referencia.
"""
import os
import sys

def cargar_genoma(path):
    """
    Carga y concatena la secuencia del genoma desde un FASTA.

    Args:
        path (str): Ruta al archivo FASTA (ej. data/genome_ecoli.fna).
    Returns:
        str: Secuencia completa sin líneas de cabecera.
    Exits:
        1 si el archivo no existe o la secuencia resultante está vacía.
    """
    if not os.path.isfile(path):
        sys.exit(f"ERROR: No existe el archivo de genoma: {path}")
    seq = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue
            seq.append(line.strip())
    genome = ''.join(seq)
    if not genome:
        sys.exit("ERROR: El FASTA de genoma está vacío.")
    print(f"✔ Genoma cargado ({len(genome)} bases)")
    return genome