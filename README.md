# Análisis de Picos de Unión de Factores de Transcripción en *Escherichia coli*

**Autor:** Mario Alejandro Samanó Basilio
**Repositorio:** `peak_analisis`

## 📂 Estructura de Carpetas

```
.
├── LICENSE
├── data
│   ├── E_coli_K12_MG1655_U00096.3.txt    # Genoma completo en FASTA
│   ├── U00096.3.bfile                    # Índice binario del genoma
│   └── union_peaks_file.tsv             # Coordenadas de picos (TSV)
├── doc
│   ├── README_TF_Binding_Project.md     # Este documento adaptado para TFs
│   ├── detalles_proyecto_actualizado.md # Parámetros, criterios y ejemplos de salida
│   └── test_cases_actualizado.md        # Casos de prueba y resultados esperados
├── results
│   └── secuencias.fasta                 # Salida FASTA consolidada
└── src
    ├── extract_fasta.py                 # Lógica de recorte FASTA
    ├── genome.py                        # Lectura e indexación del genoma
    ├── io_utils.py                     # Funciones genéricas de I/O y logging
    ├── main.py                          # Punto de entrada (CLI)
    └── peaks.py                         # Procesamiento y validación de picos
```

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Requisitos y Datos](#requisitos-y-datos)
3. [Propósito](#propósito)
4. [Instalación y Ejecución](#instalación-y-ejecución)
5. [Parámetros Opcionales](#parámetros-opcionales)
6. [Prácticas de Desarrollo](#prácticas-de-desarrollo)
7. [Hoja de Ruta (Roadmap)](#hoja-de-ruta-roadmap)
8. [Licencia](#licencia)

---

## 🔍 Visión General

En estudios de **ChIP-seq**, los factores de transcripción (TFs) se unen a regiones específicas del genoma. Este proyecto procesa las coordenadas de picos de unión de **144** TFs en *E. coli* K-12 MG1655, extrae las secuencias de ADN correspondientes y las consolida en un único archivo FASTA para análisis posteriores (motif discovery, machine learning, etc.).

* **Entrada:** TSV con columnas como `Dataset_Id`, `TF_name`, `peak_start`, `peak_end`, `peak_center` y métricas de enriquecimiento.
* **Salida:** `results/secuencias.fasta` con cabeceras `>TF_name|peak_number|chr: start-end`.

---

## ⚙️ Requisitos y Datos

* **Lenguaje:** Python 3.8+
* **Dependencias principales:**

  ```bash
  pip install -r requirements.txt  # pandas, biopython, tqdm, pytest
  ```
* **Almacenamiento:** \~50 MB (genoma + índices).
* **Archivos en `data/`**:

  * `E_coli_K12_MG1655_U00096.3.txt`: FASTA del cromosoma principal.
  * `U00096.3.bfile`: Binario generado por `genome.index()` para lectura rápida.
  * `union_peaks_file.tsv`: TSV con datos agregados de MACS2 para cada TF.

---

## 🎯 Propósito

1. **Indexar el genoma** (`genome.py`): velocidad de acceso aleatorio a regiones de ADN.
2. **Parsear y validar picos** (`peaks.py`): descartar entradas fuera de rango o con coordenadas invertidas.
3. **Extraer secuencias** (`extract_fasta.py`): recortar el FASTA usando índices y coordenadas.
4. **Registrar eventos** (`io_utils.py`): logging de advertencias y errores en `results/log.txt`.
5. **Generar salida** (`main.py`): ensamblar el flujo y escribir `results/secuencias.fasta`.

---

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/MarioASamano/peak_analisis.git
   cd peak_analisis
   ```
2. **Crear entorno virtual**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Correr el pipeline**

   ```bash
   python src/main.py \
     --fasta data/E_coli_K12_MG1655_U00096.3.txt \
     --index data/U00096.3.bfile \
     --peaks data/union_peaks_file.tsv \
     --out results/secuencias.fasta
   ```
4. **Salida esperada**

   * `results/secuencias.fasta`: un FASTA con \~144 entradas (uno por pico).
   * `results/log.txt`: registro de validaciones y errores.

---

## 🔧 Parámetros Opcionales

* `--window`: tamaño de flanco alrededor del `peak_center` (default: 0).
* `--min-length` / `--max-length`: filtrar secuencias por longitud.
* `--verbose`: activa salida detallada en consola.

```bash
python src/main.py --help
```

---

## 🛠️ Prácticas de Desarrollo

* **Control de Versiones:** Git/GitHub, GitFlow y Pull Requests con revisiones.
* **Calidad de Código:** PEP 8 (con `flake8`), docstrings Napoléon y typing hints.
* **Logs y Manejo de Errores:** uso de módulo `logging` para trazabilidad.
* **Pruebas:** framework `pytest`, cobertura >80 %, casos en `doc/test_cases_actualizado.md` y carpeta `tests/`.
* **Integración Continua:** sugerido GitHub Actions para ejecutar tests y linter en cada PR.

---

## 📅 Hoja de Ruta (Roadmap)

| Hito     | Fecha Aprox. | Descripción                                |
| -------- | ------------ | ------------------------------------------ |
| **v1.0** | 01-Jun-2025  | Pipeline básico de extracción y validación |
| **v1.1** | 05-Jun-2025  | Agregar opciones de flancos y filtros      |
| **v1.2** | 10-Jun-2025  | Documentación completa en `doc/`           |
| **v2.0** | 15-Jun-2025  | Integración de CI/CD y tests adicionales   |

---

## 📄 Licencia

Este proyecto está bajo la **MIT License**. Consulta `LICENSE` para detalles completos.
