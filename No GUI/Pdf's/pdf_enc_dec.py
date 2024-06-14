# v1.0
# PDF Encrypter
# Dependency pikepdf
# MIT license -- free to use as you want, cheers

# Author: Voldwyce

import pikepdf
import os

def main():
    print("PDF Encrypter/Decrypter")
    print("1. Encrypt")
    print("2. Decrypt")
    option = input("Enter option: ")
    if option == "1":
        encrypt()
    elif option == "2":
        decrypt()
    else:
        print("Invalid option")

def encrypt():
    print("PDF Encrypter")
    path = input("Ruta absoluta o relativa del pdf: ")
    owner_password = input("Enter owner password: ")
    user_password = input("Enter user password: ")
    output_file_name = path , "_encrypted.pdf"

    try:
        pdf = pikepdf.Pdf.open(path)
        
        # R=4 is 128 aes encryption // R=6 is 256 aes encryption
        pdf.save(output_file_name, encryption=pikepdf.Encryption(owner=owner_password, user=user_password, R=4)) 
        pdf.close()
        print("Documento encryptado con éxito")
        ## Preguntar si quiere borrar el documento original
        option = input("¿Desea borrar el documento original? (y/n): ")
        if option == "y":
            os.remove(path)
            print("Documento original borrado con éxito")
    except:
        print("Error al encryptar el documento")


def decrypt():
    print("PDF Decrypter")
    path = input("Ruta absoluta o relativa del pdf: ")
    password = input("Enter the owner password: ")
    output_file_name = path , "_decrypted.pdf"
    pdf = pikepdf.open(path, password=password)
    pdf.save(output_file_name)
    ## Preguntar si quiere borrar el documento original
    option = input("¿Desea borrar el documento original? (y/n): ")
    if option == "y":
        os.remove(path)
        print("Documento original borrado con éxito")



if __name__ == "__main__":
    main()