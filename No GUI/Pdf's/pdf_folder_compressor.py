<<<<<<< HEAD:No GUI/Pdf's/pdf_folder_compressor.py
# v1.0
# Modified version of theeko74 simple script
# Dependency Ghostscript
# MIT license -- free to use as you want, cheers

# Author: Voldwyce

import argparse
import os
import shutil
import subprocess
import time
import os.path

CALIDAD = {
    0: "/default",
    1: "/prepress",
    2: "/printer",
    3: "/ebook",
    4: "/screen"
}


def comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion):
    try:
        gs = obtener_ruta_ghostscript()
        subprocess.call([
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={CALIDAD[nivel_compresion]}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-q",
            f"-sOutputFile={archivo_salida}",
            archivo_entrada,
        ])
    except Exception as e:
        print(f"Error al comprimir {archivo_entrada}: {str(e)}")
        

def obtener_ruta_ghostscript():
    # nombres_gs = ["gs", "gswin32", "gswin64"]
    nombres_gs = ["gswin64c"]
    for nombre in nombres_gs:
        if shutil.which(nombre):
            return shutil.which(nombre)
    raise FileNotFoundError(
        f"No se encontró el ejecutable de GhostScript en la ruta ({'/'.join(nombres_gs)})"
    )

def mover_pdfs(input_folder, output_folder, successfull_folder):
    ts = time.time()
    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
                os.utime(archivo_entrada, (ts, ts))
                ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                shutil.copy(archivo_entrada, ruta_archivo_realizado)
                shutil.move(archivo_entrada, archivo_salida)


def comprimir_carpeta(input_folder, output_folder, successfull_folder, nivel_compresion=0):
    # Verificar y crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Verificar y crear la carpeta de "backup" si no existe
    if not os.path.exists(successfull_folder):
        os.makedirs(successfull_folder)

    archivos_comprimidos = 0
    tam_carpeta = 0
    tam_carpeta_final = 0

    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
            if archivo_entrada.lower().endswith('.pdf'):
                tam_inicial = os.path.getsize(archivo_entrada)
                try:
                    comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion)
                    tam_final = os.path.getsize(archivo_salida)
                    ratio = 1 - (tam_final / tam_inicial)

                    if tam_final < tam_inicial:
                        archivos_comprimidos += 1
                        print("")
                        print(f" Archivo: {archivo_entrada}")
                        print(f" Ratio de compresión: {ratio:.0%}")
                        print(f" Tamaño final del archivo: {tam_inicial / 1000000:.5f}MB -> {tam_final / 1000000:.5f}MB")
                        print("")

                        # Mover archivo original a la carpeta de "backup"
                        ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                        shutil.move(archivo_entrada, ruta_archivo_realizado)
                        tam_carpeta += tam_inicial
                        tam_carpeta_final += tam_final

                    else:
                        # Si el tamaño final es mayor al inicial, se vuelve a comprimir con un nivel de compresión mayor
                        comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion + 1)
                        tam_final_nuevo = os.path.getsize(archivo_salida)
                        ratio_nuevo = 1 - (tam_final_nuevo / tam_inicial)

                        if tam_final_nuevo < tam_inicial:
                            archivos_comprimidos += 1
                            print("")
                            print(f" Archivo: {archivo_entrada}")
                            print(f" Ratio de compresión (nuevo): {ratio_nuevo:.0%}")
                            print(f" Tamaño final del archivo (nuevo): {tam_inicial / 1000000:.5f}MB -> {tam_final_nuevo / 1000000:.5f}MB")
                            print("")

                            # Mover archivo original a la carpeta de "backup"
                            ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                            shutil.move(archivo_entrada, ruta_archivo_realizado)
                            tam_carpeta += tam_inicial
                            tam_carpeta_final += tam_final_nuevo

                except Exception as e:
                    # Captura de excepción si la compresión falla
                    print(f"Error al comprimir {archivo_entrada}: {str(e)}")

    ratio_carpeta = 0
    if tam_carpeta + tam_carpeta_final > 0:
        ratio_carpeta = ratio_carpeta = 1 - (tam_carpeta_final / tam_carpeta)

    print(" **************************************************************")
    print(f" Total de archivos comprimidos: {archivos_comprimidos}")
    print(f" Tamaño final de la compresion: {tam_carpeta / 1000000:.5f} -> {tam_carpeta_final / 1000000:.5f}")
    print(f" Ratio final de compresión: {ratio_carpeta:.0%}")
    print(" **************************************************************")
    mover_pdfs(input_folder, output_folder, successfull_folder)


def main():

    print("Compresor de PDF")
    print("Ingrese la ruta de la carpeta de entrada que contiene los archivos PDF")
    pathIn = input("Ruta: ")
    print("Ingrese la ruta de la carpeta de salida para los archivos comprimidos")
    pathOut = input("Ruta: ")
    print("Ingrese la ruta de la carpeta donde se moverán los archivos originales")
    pathBackup = input("Ruta: ")
    print("Nivel de compresión")
    print("0. Default")
    print("1. Prepress")
    print("2. Printer (Recomendado)")
    print("3. Ebook")
    print("4. Screen")
    power = input("Opción: ")

    # Ejecutar compresión de la carpeta
    comprimir_carpeta(pathIn, pathOut, pathBackup, nivel_compresion=int(power))

if __name__ == "__main__":
    main()
=======
# v1.0
# Modified version of theeko74 simple script
# Dependency Ghostscript
# MIT license -- free to use as you want, cheers

# Author: Voldwyce

import argparse
import os
import shutil
import subprocess
import time
import os.path

CALIDAD = {
    0: "/default",
    1: "/prepress",
    2: "/printer",
    3: "/ebook",
    4: "/screen"
}


def comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion):
    try:
        gs = obtener_ruta_ghostscript()
        subprocess.call([
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={CALIDAD[nivel_compresion]}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-q",
            f"-sOutputFile={archivo_salida}",
            archivo_entrada,
        ])
    except Exception as e:
        print(f"Error al comprimir {archivo_entrada}: {str(e)}")
        

def obtener_ruta_ghostscript():
    # nombres_gs = ["gs", "gswin32", "gswin64"]
    nombres_gs = ["gswin64c"]
    for nombre in nombres_gs:
        if shutil.which(nombre):
            return shutil.which(nombre)
    raise FileNotFoundError(
        f"No se encontró el ejecutable de GhostScript en la ruta ({'/'.join(nombres_gs)})"
    )

def mover_pdfs(input_folder, output_folder, successfull_folder):
    ts = time.time()
    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
                os.utime(archivo_entrada, (ts, ts))
                ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                shutil.copy(archivo_entrada, ruta_archivo_realizado)
                shutil.move(archivo_entrada, archivo_salida)


def comprimir_carpeta(input_folder, output_folder, successfull_folder, nivel_compresion=0):
    # Verificar y crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Verificar y crear la carpeta de "backup" si no existe
    if not os.path.exists(successfull_folder):
        os.makedirs(successfull_folder)

    archivos_comprimidos = 0
    tam_carpeta = 0
    tam_carpeta_final = 0

    for file_name in os.listdir(input_folder):
        archivo_entrada = os.path.join(input_folder, file_name)
        archivo_salida = os.path.join(output_folder, file_name)

        if os.path.isfile(archivo_entrada):
            if archivo_entrada.lower().endswith('.pdf'):
                tam_inicial = os.path.getsize(archivo_entrada)
                try:
                    comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion)
                    tam_final = os.path.getsize(archivo_salida)
                    ratio = 1 - (tam_final / tam_inicial)

                    if tam_final < tam_inicial:
                        archivos_comprimidos += 1
                        print("")
                        print(f" Archivo: {archivo_entrada}")
                        print(f" Ratio de compresión: {ratio:.0%}")
                        print(f" Tamaño final del archivo: {tam_inicial / 1000000:.5f}MB -> {tam_final / 1000000:.5f}MB")
                        print("")

                        # Mover archivo original a la carpeta de "backup"
                        ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                        shutil.move(archivo_entrada, ruta_archivo_realizado)
                        tam_carpeta += tam_inicial
                        tam_carpeta_final += tam_final

                    else:
                        # Si el tamaño final es mayor al inicial, se vuelve a comprimir con un nivel de compresión mayor
                        comprimir_pdf(archivo_entrada, archivo_salida, nivel_compresion + 1)
                        tam_final_nuevo = os.path.getsize(archivo_salida)
                        ratio_nuevo = 1 - (tam_final_nuevo / tam_inicial)

                        if tam_final_nuevo < tam_inicial:
                            archivos_comprimidos += 1
                            print("")
                            print(f" Archivo: {archivo_entrada}")
                            print(f" Ratio de compresión (nuevo): {ratio_nuevo:.0%}")
                            print(f" Tamaño final del archivo (nuevo): {tam_inicial / 1000000:.5f}MB -> {tam_final_nuevo / 1000000:.5f}MB")
                            print("")

                            # Mover archivo original a la carpeta de "backup"
                            ruta_archivo_realizado = os.path.join(successfull_folder, file_name)
                            shutil.move(archivo_entrada, ruta_archivo_realizado)
                            tam_carpeta += tam_inicial
                            tam_carpeta_final += tam_final_nuevo

                except Exception as e:
                    # Captura de excepción si la compresión falla
                    print(f"Error al comprimir {archivo_entrada}: {str(e)}")

    ratio_carpeta = 0
    if tam_carpeta + tam_carpeta_final > 0:
        ratio_carpeta = ratio_carpeta = 1 - (tam_carpeta_final / tam_carpeta)

    print(" **************************************************************")
    print(f" Total de archivos comprimidos: {archivos_comprimidos}")
    print(f" Tamaño final de la compresion: {tam_carpeta / 1000000:.5f} -> {tam_carpeta_final / 1000000:.5f}")
    print(f" Ratio final de compresión: {ratio_carpeta:.0%}")
    print(" **************************************************************")
    mover_pdfs(input_folder, output_folder, successfull_folder)


def main():

    print("Compresor de PDF")
    print("Ingrese la ruta de la carpeta de entrada que contiene los archivos PDF")
    pathIn = input("Ruta: ")
    print("Ingrese la ruta de la carpeta de salida para los archivos comprimidos")
    pathOut = input("Ruta: ")
    print("Ingrese la ruta de la carpeta donde se moverán los archivos originales")
    pathBackup = input("Ruta: ")
    print("Nivel de compresión")
    print("0. Default")
    print("1. Prepress")
    print("2. Printer (Recomendado)")
    print("3. Ebook")
    print("4. Screen")
    power = input("Opción: ")

    # Ejecutar compresión de la carpeta
    comprimir_carpeta(pathIn, pathOut, pathBackup, nivel_compresion=int(power))

if __name__ == "__main__":
    main()
>>>>>>> 26b3e9e9014084ca1e6bde66880095647df41d49:Pdf's/pdf_folder_compressor.py
