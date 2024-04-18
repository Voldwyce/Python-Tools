# v1.0
# Modified version of theeko74 simple script
# Dependency Ghostscript & shutil

# Author: Voldwyce

import argparse
import os.path
import shutil
import subprocess
import sys


def compress(input_file_path, output_file_path, power=0):
    """Function to compress PDF via Ghostscript command line interface"""
    quality = {
        0: "/default",
        1: "/prepress",
        2: "/printer",
        3: "/ebook",
        4: "/screen"
    }

    # Revisar si el archivo existe
    if not os.path.isfile(input_file_path):
        print("Error: ruta o archivo no encontrado", input_file_path)
        sys.exit(1)

    # Revision de nivel de compresion
    if power < 0 or power > len(quality) - 1:
        print("Error: nivel de compresion no valido, escribe pdfc -h para ver opciones.", power)
        sys.exit(1)

    # Revisar si el archivo es un PDF
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file is not a PDF.", input_file_path)
        sys.exit(1)

    gs = get_ghostscript_path()
    print("Comprimir PDF...")
    initial_size = os.path.getsize(input_file_path)
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(output_file_path),
            input_file_path,
        ]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("% De compresison {0:.0%}.".format(ratio))
    print("{0:.5f}MB".format(initial_size / 1000000), "--> {0:.5f}MB".format(final_size / 1000000))
    print("Finalizado.")


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No se encontro la ruta del ghostscript en ({'/'.join(gs_names)})"
    )


def main():

    print("PDF Compressor")
    pathIn = input("Ruta absoluta o relativa del pdf: ")
    print("Generar archivo de salida o reemplazar el original")
    print("1. Generar archivo de salida")
    print("2. Reemplazar archivo original")
    option = input("Enter option: ")
    if option == "1":
        pathOut = input("Ruta absoluta o relativa del archivo de salida: ")
    elif option == "2":
        pathOut = pathIn
    else:
        print("Invalid option")
        sys.exit(1)
    print("Nivel de compresion")
    print("0. Default")
    print("1. Prepress")
    print("2. Printer (Recomendado)")
    print("3. Ebook")
    print("4. Screen")
    power = input("Enter option: ")

    print("¿Generar backup del archivo original?")
    print("1. Si")
    print("2. No")
    option = input("Enter option: ")
    if option == "1":
        backup = True
    elif option == "2":
        backup = False
    else:
        print("Invalid option")
        sys.exit(1)

    print("¿Abrir archivo despues de comprimir?")
    print("1. Si")
    print("2. No")
    option = input("Enter option: ")
    if option == "1":
        open = True
    elif option == "2":
        open = False
    else:
        print("Invalid option")
        sys.exit(1)

    # Archivo de salida por defecto si no se especifica
    if not pathOut:
        pathOut = "temp.pdf"

    # Run
    compress(pathIn, pathOut, power=int(power))

    # Si no se especifica archivo de salida, se sobreescribe el original
    if not pathOut:
        if backup:
            shutil.copyfile(pathIn, pathIn.replace(".pdf", "_BACKUP.pdf"))
        shutil.copyfile(pathOut, pathIn)
        os.remove(pathOut)

    # Opcion para abrir el archivo despues de comprimir
    if open:
        os.startfile(pathOut)


if __name__ == "__main__":
    main()