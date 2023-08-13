import streamlit as st
import requests
import json
import os
import re
from dotenv import load_dotenv
from PIL import Image

# Cargar variables de entorno desde el archivo .env
load_dotenv()

YOUR_GENERATED_SECRET = os.getenv('BESTBANNER_SECRET')
MAIN_DIR = "./data/"
def generate_banner(titulo, texto):
    # Crear payload de datos
    data = {
        "data": [
            {"text": f"{titulo} {texto}"}
        ]
    }

    headers = {
        "x-api-key": f"token {YOUR_GENERATED_SECRET}",
        "content-type": "application/json",
    }

    # Realizar solicitud POST
    response = requests.post(
        "https://api.bestbanner.jina.ai/v1/generate",
        headers=headers,
        data=json.dumps(data)
    )

    return response

def download_image(url,filename):

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"La imagen ha sido descargada y guardada como {filename}")
    else:
        print("Error al descargar la imagen")
def save_image_locally(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(f"./data/{filename}", "wb") as f:
            f.write(response.content)

        # Guardar una copia en la carpeta local "data"
        with open(f"./data/generated_{filename}", "wb") as f:
            f.write(response.content)

def extract_number_from_filename(filename):
    match = re.search(r'_(\d+)', filename)
    if match:
        return +int(match.group(1))  # Agregar el signo negativo para ordenar de mayor a menor
    else:
        return 0

def main():
    st.title("Generador de Banners")

    # Obtener el título y el texto del artículo desde el usuario
    titulo = st.text_input("Título del artículo:")
    texto = st.text_area("Texto del artículo:")

    # Agregar un botón para ejecutar la solicitud POST
    if st.button("Ejecutar"):
        response = generate_banner(titulo, texto)

        # Mostrar resultados
        st.subheader("Respuesta del Servidor:")
        st.write(f"Código de estado: {response.status_code}")
        st.write(f"Mensaje: {response.reason}")
        st.write("Texto de respuesta:")
        st.code(response.text)

        # Imprimir la respuesta completa en la consola
        print(response.json())

        for banner in response.json()["result"][0]["banners"] :
            # Guardar una copia de la imagen generada en la carpeta local "data"
            #image_url = response.json()["result"][0]["banners"][0]["url"]
            image_url = banner["url"]
            print(image_url)
            download_image(image_url,str(MAIN_DIR) + str(os.path.basename(image_url)))
        #save_image_locally(image_url)

    st.title("Galería de imágenes generadas")

    image_files = os.listdir("./data")
    image_files = sorted(image_files, key=extract_number_from_filename, reverse=True)
    num_columns = 4
    image_groups = [image_files[i:i+num_columns] for i in range(0, len(image_files), num_columns)]

    for group in image_groups:
        columns = st.columns(4)
        for i, image_file in enumerate(group):
            if image_file.endswith(".png"):
                img_path = os.path.join("./data", image_file)
                image = Image.open(img_path)
                resized_image = image.resize((300, 300))

                # Mostrar la imagen en la columna correspondiente
                with columns[i]:
                    st.image(resized_image, caption=image_file, width=300, use_column_width=True, clamp=True)

if __name__ == "__main__":
    main()
