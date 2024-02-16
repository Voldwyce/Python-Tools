# v1.0
# Modified version of theeko74 simple script
# Dependency Ghostscript & shutil
# MIT license -- free to use as you want, cheers

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
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="Ruta absoluta o relativa del archivo PDF ")
    parser.add_argument("-o", "--out", help="Ruta absoluta o relativa del archivo de salida")
    parser.add_argument("-c", "--compress", type=int, help="Nivel de compresion (0-4)")
    parser.add_argument("-b", "--backup", action="store_true", help="Crear copia de seguridad del archivo original")
    parser.add_argument("--open", action="store_true", default=False, help="Abrir el archivo despues de comprimir")
    args = parser.parse_args()

    # Compresion por defecto si no se especifica
    if not args.compress:
        args.compress = 2
    # Archivo de salida por defecto si no se especifica
    if not args.out:
        args.out = "temp.pdf"

    # Run
    compress(args.input, args.out, power=args.compress)

    # Si no se especifica archivo de salida, se sobreescribe el original
    if args.out == "temp.pdf":
        if args.backup:
            shutil.copyfile(args.input, args.input.replace(".pdf", "_BACKUP.pdf"))
        shutil.copyfile(args.out, args.input)
        os.remove(args.out)

    # Opcion para abrir el archivo despues de comprimir
    if args.open:
        if args.out == "temp.pdf" and args.backup:
            subprocess.call(["open", args.input])
        else:
            subprocess.call(["open", args.out])


if __name__ == "__main__":
    main()