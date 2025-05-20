"""
Funciones auxiliares para escribir archivos FASTA.
"""
import os

def guardar_fasta_por_tf(genome, peaks_by_tf, outdir):
    """
    Por cada TF, extrae sus secuencias del genoma y crea un FASTA.

    Args:
        genome (str): Secuencia completa del genoma.
        peaks_by_tf (dict): {tf_name: [(start,end), ...]}.
        outdir (str): Carpeta de salida (ej. results/).
    """
    os.makedirs(outdir, exist_ok=True)
    for tf, intervals in peaks_by_tf.items():
        ruta = os.path.join(outdir, f"{tf}_peaks.fasta")
        with open(ruta, 'w') as out:
            for idx, (start, end) in enumerate(intervals, 1):
                seq = genome[start:end]
                out.write(f">{tf}_pico_{idx}_{start}_{end}\n{seq}\n")
        print(f"  • {len(intervals)} secuencias para {tf} → {ruta}")