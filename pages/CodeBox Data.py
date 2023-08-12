import streamlit as st
import openai
from dotenv import load_dotenv
import os
import asyncio

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la clave de API de OpenAI desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

from codeinterpreterapi import CodeInterpreterSession


async def generar_codigo(indicaciones):
    # Crea una sesión
    session = CodeInterpreterSession()
    await session.start()

    # Genera una respuesta en función de las indicaciones del usuario
    response = await session.generate_response(indicaciones)

    # Muestra el código generado en una sección de consola
    st.subheader("Consola de Código Generado:")
    st.code("AI: " + response.content, language="python")

    # Muestra la imagen generada
    for file in response.files:
        st.subheader("Imagen Generada:")
        st.image(file.content)

    # Termina la sesión
    await session.stop()


def main():
    st.title("Generador de Código con Indicaciones")

    # Campo de entrada para las indicaciones del usuario
    indicaciones = st.text_input("Indicaciones", "Escribe aquí lo que deseas generar")

    # Botón para generar el código
    if st.button("Generar Código"):
        # Genera el código utilizando asyncio
        asyncio.run(generar_codigo(indicaciones))


if __name__ == "__main__":
    main()


