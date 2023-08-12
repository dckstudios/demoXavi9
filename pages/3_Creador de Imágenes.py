import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from jinaai import JinaAI

# Cargar variables de entorno desde el archivo .env
load_dotenv()

jinaai = JinaAI(
    secrets = {
        'promptperfect-secret': os.getenv('PROMPTPERFECT_SECRET'),
        'scenex-secret': os.getenv('SCENEX_SECRET'),
        'rationale-secret': os.getenv('RATIONALE_SECRET'),
        'jinachat-secret': os.getenv('JINACHAT_SECRET'),
        'bestbanner-secret': os.getenv('BESTBANNER_SECRET'),
    }
)


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

    # Mostrar imágenes generadas anteriores
    st.subheader("Imágenes generadas anteriores:")
    previous_images = st.empty()

    # Obtener imágenes generadas anteriores
    previous_images_response = requests.get("https://api.bestbanner.jina.ai/v1/images")
    if previous_images_response.status_code == 200 and previous_images_response.text:
        previous_images_data = json.loads(previous_images_response.text).get("data", [])
        if previous_images_data:
            for i, image_data in enumerate(previous_images_data[::-1]):
                image_url = image_data.get("url")
                if image_url:
                    image_response = requests.get(image_url)
                    img = Image.open(BytesIO(image_response.content))
                    previous_images.image(img, caption=f"Imagen {i+1}")
    else:
        st.write("Error al obtener las imágenes generadas anteriores.")

if __name__ == "__main__":
    main()
