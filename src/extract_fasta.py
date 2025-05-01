"""
Script para extraer los picos de unión o "Union Peaks" del genoma de E. Coli.
Inputs:
- genoma_ecoli.fna : Genoma de referencia en formato FASTA
- union_peaks_file.tsv : Coordenadas de picos (cols: TF_name, Peak_start, Peak_end)

Output:
- results/secuencias.fasta : Secuencias extraídas (requiere carpeta preexistente) 
:)
"""

def cargar_genoma(): #----------------------------------------------------------- Carga el genoma desde genoma_ecoli.fna
    
    """
    Carga y concatena el genoma completo desde un archivo FASTA.
    
    Returns:
        str: Cadena con la secuencia completa del genoma sin cabeceras.
    
    Exits:
        1: Si el archivo no existe o está vacío.
    """
     
    with open('E_coli_K12_MG1655_U00096.3.txt', 'r') as f:
        genoma = ''.join(linea.strip() for linea in f if linea.strip() and not linea.startswith('>'))
    
    if not genoma:
        print("ERROR: El archivo genoma_ecoli.fna está vacío, intentalo con otro archivo :(")
        exit(1)
        
    print(f"Genoma cargado (longitud: {len(genoma)} bases)")
    return genoma

def leer_picos(): #----------------------------------------------------------- Lee el archivo TSV con los picos de union (las "coordenadas")
    """
    Procesa un archivo TSV con coordenadas de picos de ChIP-seq.
    
    Returns:
        list: Lista de tuplas con (nombre_TF, inicio, fin) para cada pico.
    
    Exits:
        1: Si el archivo no existe, tiene formato incorrecto o contiene datos inválidos.
    """
     
    with open('union_peaks_file.tsv', 'r') as f:

        next(f)
        lineas = [linea.strip() for linea in f if linea.strip()]
    
    picos = []
    for num_linea, linea in enumerate(lineas, 2):
        partes = linea.split('\t')
        
        if len(partes) < 1:
            print(f"ERROR Línea: {num_linea}")
            exit(1)
            
        tf_name = partes[0]
        start = int(float(partes[3]))
        end = int(float(partes[5]))
        picos.append((tf_name, start, end))
    
    if not picos:
        print("ERROR: No se encontraron picos válidos")
        exit(1)
        
    print(f"{len(picos)} picos encontrados :D")
    return picos

def extraer_secuencias(picos, genoma): #------------------------------------------------------------ Extrae secuencias del genoma
    """
    Extrae fragmentos genómicos basados en coordenadas de picos.
    
    Args:
        picos (list): Lista de tuplas (nombre_TF, inicio, fin).
        genoma (str): Secuencia genómica completa.
    
    Returns:
        list: Lista de tuplas con (nombre_TF, secuencia_extraída).
    
    Exits:
        1: Si las coordenadas son inválidas (fuera de rango o inicio >= fin).
    """

    secuencias = []
    largo_genoma = len(genoma)
    
    for nombre, inicio, fin in picos:
        if inicio < 0 or fin > largo_genoma:
            print(f"ERROR: Coordenadas fuera de rango para {nombre}")
            exit(1)
            
        if inicio >= fin: # <--------- Solo por si acaso jaja 
            print(f"ERROR: Inicio debe ser menor que fin para {nombre}")
            exit(1)
            
        secuencias.append((nombre, genoma[inicio:fin]))
    
    print(f"{len(secuencias)} secuencias extraídas")
    return secuencias

def guardar_secuencias(secuencias): #-------------------------------------------------------------- Guardado de secuencia 
    """
    Guarda todas las secuencias en results/secuencias.fasta
    Es decir, redirecciona el archivo de salida u "output file" al directorio results 
    """
    archivo_salida = "results/secuencias.fasta"
    
    with open(archivo_salida, 'w') as f:
        for i, (nombre, secuencia) in enumerate(secuencias, 1):
            f.write(f">{nombre}_pico_{i}\n{secuencia}\n")
    
    print(f"Archivo creado: {archivo_salida}")

def main():
    print("\n=== Extracción de Secuencias FASTA :D ===")
    print("Asegúrate de tener:")
    print("1. El archivo genoma_ecoli.fna")
    print("2. El archivo union_peaks_file.tsv")
    print("3. Una carpeta 'results' creada manualmente\n")
    
    genoma = cargar_genoma()
    picos = leer_picos()
    secuencias = extraer_secuencias(picos, genoma)
    
    guardar_secuencias(secuencias)
    print("\nProceso completado")

if __name__ == "__main__":
    main()