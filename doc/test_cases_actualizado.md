### Casos de Prueba para el Módulo 1: Extractor y Creador de Secuencias FASTA


1.  **Caso: Archivo del genoma no se encuentra.**
    
    -   **Entradas:**
        -   Ruta incorrecta o inexistente para el archivo FASTA del genoma.
        -   Archivo de picos válido.
        -   Directorio de salida.
    -   **Esperado:** `"Error: Genome file not found"`
    
    ```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
    ```
    ```
    Error: "Ecoli.fna" genome file not found
    ```
2.  **Caso: Archivo de picos vacío.**
    
    -   **Entradas:**
        -   Archivo de picos vacío.
        -   Archivo FASTA del genoma.
        -   Directorio de salida.
    -   **Esperado:** `"Error: the peak file is empty."`

 ```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
```
  
```
Error: the peak file is empty
```
3. **Caso: Archivo de E. Coli**
Verificar que los archivos sean los correctos, en caso de cambiar el genoma de E. Coli por el de otros organismos, ya que si el formato es el correcto no va a marcar ningún error

4. **Archivos de genoma vacíos**

Verificar que los archivos de los genómas contengan información, ya que de no ser el caso se produciría un error.


5.  **Caso: Posiciones `Peak_start` y `Peak_end` fuera del rango del genoma.**
    
    -   **Entradas:**
        -   Archivo de picos con algunas posiciones `Peak_start` y `Peak_end` fuera del tamaño del genoma.
        -   Archivo FASTA del genoma válido.
        -   Directorio de salida.
    -   **Esperado:**
        -   El sistema debe imprimir un mensaje de advertencia: `"Warning: Some peaks are bigger than the genome". Check the log.out file`
        
        -   Generar un archivo de log indicando los picos fuera de rango. El archivo debe contener las líneas del archivo de picos que tienen problemas.

```python
    mk_fasta_from_peaks.py -i peak_file.txt -g Ecoli.fna -o fasta_peaks/ 
```

```bash
ls
```

```bash
log.out
fasta_peaks/
```/).
```
---
1. Verificar que los archivos sean los correctos, en caso de cambiar el genoma de E. Coli por el de otros organismos, ya que si el formato es el correcto no va a marcar ningún error 

2.  Archivos de genoma vacíos 

