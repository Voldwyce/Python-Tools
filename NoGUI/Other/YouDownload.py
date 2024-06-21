from pytube import YouTube
import argparse
import os

def YouDownload(url, download_type):
    try:
        yt = YouTube(url)

        if download_type == "Video":
            stream = yt.streams.get_highest_resolution()
        elif download_type == "Audio":
            stream = yt.streams.filter(only_audio=True).first()

        if stream:
            print(f"Descargando {stream.title}...")
            stream.download(output_path=os.getcwd())
            print("Descarga completada.")
        else:
            print("No se encontró ningún stream disponible para descargar.")
    except Exception as e:
        print(f"Error al descargar el video: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Descargador de videos de YouTube")
    parser.add_argument("url", type=str, help="URL del video de YouTube")
    parser.add_argument("--type", choices=["Video", "Audio"], default="Video", help="Tipo de descarga (default: Video)")
    args = parser.parse_args()

    YouDownload(args.url, args.type)
