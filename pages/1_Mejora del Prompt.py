import os
import streamlit as st
from jinaai import JinaAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

jinaai = JinaAI(
    secrets={
        'promptperfect-secret': os.getenv('PROMPTPERFECT_SECRET'),
        'scenex-secret': os.getenv('SCENEX_SECRET'),
        'rationale-secret': os.getenv('RATIONALE_SECRET'),
        'jinachat-secret': os.getenv('JINACHAT_SECRET'),
        'bestbanner-secret': os.getenv('BESTBANNER_SECRET'),
    }
)

st.title("Prompt Optimization")

# Input
prompt_input = st.text_area("Enter the prompt:", "Eres un chatbot asistente para el equipo de Comercial , deberá ser capaz de dar explicaciones sobre las actividades que se realizan en los sectores industriales.", height=200)

# Sidebar
# Sidebar
st.sidebar.title("Opciones")

st.sidebar.markdown("**Modelo objetivo:**")
st.sidebar.markdown("El modelo de lenguaje al que se dirigirá la optimización.")

target_model = st.sidebar.selectbox("", ['chatgpt', 'gpt-4', 'stablelm-tuned-alpha-7b', 'claude', 'cogenerate', 'text-davinci-003', 'dalle', 'sd', 'midjourney', 'kandinsky', 'lexica'])

st.sidebar.markdown("**Características:**")
st.sidebar.markdown("Las características adicionales que se pueden aplicar a la optimización.")

features = st.sidebar.multiselect("", ['preview', 'no_spam', 'shorten', 'bypass_ethics', 'same_language', 'always_en', 'high_quality', 'redo_original_image', 'variable_subs', 'template_run'])

st.sidebar.markdown("**Iteraciones:**")
st.sidebar.markdown("El número de iteraciones que se realizarán durante la optimización.")

iterations = st.sidebar.number_input("", value=1, key="iterations")

st.sidebar.markdown("**Temperatura de vista previa:**")
st.sidebar.markdown("La temperatura de la vista previa, que afecta la aleatoriedad de las respuestas generadas.")

temperature = st.sidebar.number_input("", value=0.9, key="temperature")

st.sidebar.markdown("**TopP de vista previa:**")
st.sidebar.markdown("El límite de probabilidad acumulativa (TopP) para la vista previa.")

topP = st.sidebar.number_input("", value=0.9, key="topP")

st.sidebar.markdown("**TopK de vista previa:**")
st.sidebar.markdown("El límite superior (TopK) para la vista previa.")

topK = st.sidebar.number_input("", value=0, key="topK")

st.sidebar.markdown("**Penalización de frecuencia de vista previa:**")
st.sidebar.markdown("La penalización de frecuencia para la vista previa.")

frequencyPenalty = st.sidebar.number_input("", value=0, key="frequencyPenalty")

st.sidebar.markdown("**Penalización de presencia de vista previa:**")
st.sidebar.markdown("La penalización de presencia para la vista previa.")

presencePenalty = st.sidebar.number_input("", value=0, key="presencePenalty")

st.sidebar.markdown("**Tiempo de espera (ms):**")
st.sidebar.markdown("El tiempo máximo de espera en milisegundos para obtener una respuesta.")

timeout = st.sidebar.number_input("", value=20000, key="timeout")

# ...



# Optimization
timeout = st.sidebar.number_input("", value=20000)
if st.button("Optimize"):
    # Optimization
    prompts = jinaai.optimize(
        prompt_input,
        options={
            'targetModel': target_model,
            'features': features,
            'iterations': iterations,
            'previewSettings': {
                'temperature': temperature,
                'topP': topP,
                'topK': topK,
                'frequencyPenalty': frequencyPenalty,
                'presencePenalty': presencePenalty
            },
            'timeout': timeout,
            'target_language': "es"
        }
    )

    # Output
    optimized_prompt = prompts['results'][0]['output']

    st.write("Optimized prompt:")
    st.write(optimized_prompt)
