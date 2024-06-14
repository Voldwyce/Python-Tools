import os

def main():
    os.system('cls')
    print("Bienvenido a Python vault tools")
    print("------------------------------------")
    print("Por favor, seleccione una de las siguientes categorias:")
    print("1. Pdf's")
    print("2. Otros")
    print("3. Salir")
    print("------------------------------------")
    opcion = input("Seleccione una opcion: ")
    os.system('cls')

    match opcion:
        case "1":
            print("Estas en la categoria de Pdf's")
            print("Por favor, seleccione una de las siguientes opciones:")
            print("")
            print("1. Comprimir Pdf")
            print("2. Comprimir carpeta de Pdf's")
            print("3. Encriptar/Desencriptar Pdf")
            print("4. Volver")
            print("------------------------------------")
            opcion = input("Seleccione una opcion: ")
            os.system('cls')

            match opcion:
                ## Ejecutamos el archivo de compresion de pdf en cmd
                case "1":
                    os.system("python Pdf's/pdf_compressor.py")
                case "2":
                    os.system("python Pdf's/pdf_folder_compressor.py")
                case "3":
                    os.system("python Pdf's/pdf_enc_dec.py")
                case "4":
                    main()
                case _: 
                    print("Opcion no valida")
        case "2":
            print('Estas en la categoria de Otros')
            print("Por favor, seleccione una de las siguientes opciones:")
            print("")
            print("1. QOTD")
            print("2. Water Reminder")
            print("3. Volver")
            print("------------------------------------")
            opcion = input("Seleccione una opcion: ")
            os.system('cls')

            match opcion:
                case "1":
                    os.system("python Other/qotd.py")
                case "2":
                    tiempo = input("Cada cuanto quieres recibir el recordatorio? (en minutos): ")
                    tiempo = tiempo * 60
                    os.system("python Other/water_reminder.pyw -t " + tiempo)
                    os.system('exit')
                case "3":
                    main()
                case _:
                    print("Opcion no valida")
        case _:
            print("Opcion no valida")

if __name__ == "__main__":
    main()
