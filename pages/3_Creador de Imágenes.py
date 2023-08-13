import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import jinaai

# Cargar variables de entorno desde el archivo .env
load_dotenv()

YOUR_GENERATED_SECRET = os.getenv('BESTBANNER_SECRET')

def generate_banner(titulo, texto, estilo="default"):
    # Crear payload de datos
    data = {
        "data": [
            {"text": f"{titulo} {texto}"},
            {"style": estilo}
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

    # Descripciones de los estilos
    estilo_descripciones = {
        "default": "El estilo predeterminado no aplica un estilo específico a la pancarta.",
        "photographic": "El estilo 'fotográfico' generará pancartas que parecen fotografías.",
        "minimalist": "El estilo 'minimalista' generará pancartas con composiciones simples.",
        "flat": "El estilo 'plano' generará pancartas modernas que parecerán ilustraciones modernas."
    }

    # Obtener el estilo de la pancarta desde el usuario
    estilo = st.radio("Estilo de la pancarta:", ("default", "photographic", "minimalist", "flat"))

    # Mostrar descripción del estilo seleccionado
    st.write(estilo_descripciones[estilo])

    # Obtener el título y el texto del artículo desde el usuario
    titulo = st.text_input("Título del artículo:")
    texto = st.text_area("Texto del artículo:")

    # Agregar un botón para ejecutar la solicitud POST
    if st.button("Ejecutar"):
        response = generate_banner(titulo, texto, estilo=estilo)

        # Mostrar resultados
        st.subheader("Respuesta del Servidor:")
        st.write(f"Código de estado: {response.status_code}")
        st.write(f"Mensaje: {response.reason}")
        st.write("Texto de respuesta:")
        st.code(response.text)

    # Mostrar imágenes generadas anteriores
    st.subheader("Imágenes generadas anteriores:")
    previous_images = st.empty()

# Obtener imágenes generadas anteriores desde el API de JinaAI
    previous_images_response = jinaai.get_previous_images()

    if previous_images_response.status_code == 200 and previous_images_response.text:
        previous_images_data = previous_images_response.json().get("data", [])

        if previous_images_data:
            for i, image_data in enumerate(previous_images_data[::-1]):
                image_url = image_data.get("url")

                if image_url:
                    if is_url(image_url):
                        image_response = requests.get(image_url)
                        img = Image.open(BytesIO(image_response.content))
                        st.image(img, caption=f"Imagen {i+1}", label=f"Imagen {i+1}")
                    else:
                        st.write(f"URL inválida: {image_url}")
    else:
        st.write("Error al obtener las imágenes generadas anteriores.")

if __name__ == "__main__":
    main()