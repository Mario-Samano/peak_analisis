"""
Punto de entrada que orquesta la extracción modular de picos.
"""
import argparse
import sys
from .genome    import cargar_genoma
from .peaks     import leer_picos
from .io_utils  import guardar_fasta_por_tf



def parse_args():
    parser = argparse.ArgumentParser(
        description="Extractor modular de picos por TF"
    )
    parser.add_argument('--genome', required=True,
                        help='Archivo FASTA del genoma (data/genome_ecoli.fna)')
    parser.add_argument('--peaks', required=True,
                        help='TSV de picos (data/union_peaks_file.tsv)')
    parser.add_argument('--outdir', required=True,
                        help='Directorio para FASTA resultantes (results/)')
    return parser.parse_args()


def main():
    args = parse_args()

    genome = cargar_genoma(args.genome)
    peaks_by_tf = leer_picos(args.peaks)
    guardar_fasta_por_tf(genome, peaks_by_tf, args.outdir)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.exit(f"ERROR inesperado: {e}")