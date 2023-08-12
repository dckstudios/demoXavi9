import os
from dotenv import load_dotenv
import streamlit as st
from jinaai import JinaAI

# Cargar las variables de entorno desde el archivo .env
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

def make_decision(input, analysis_type, style):
    options = {
        'analysis': analysis_type,
        'style': style,
    }
    output = jinaai.decide(input, options)
    return output

# Configurar la página de la aplicación con el tipo de análisis, la decisión y el botón de ejecución
st.title('Analisis racionales sobre decisiones personales')
# Agregar texto explicativo debajo del título
st.markdown('## Tipos de Análisis')
st.write('Elige entre los siguientes tipos de análisis:')
st.write('- **proscons**: Proporciona los pros y contras de la decisión.')
st.write('- **swot**: Realiza un análisis DAFO, resaltando las fortalezas, debilidades, oportunidades y amenazas.')
st.write('- **multichoice**: Ofrece múltiples opciones y sus explicaciones.')
st.write('- **outcomes**: Genera un árbol de posibles resultados y sus explicaciones.')
        

ANALYSIS_TYPES = ['proscons', 'swot', 'multichoice', 'outcomes']
analysis_type = st.selectbox('Tipo de Análisis', ANALYSIS_TYPES)
decision = st.text_input('Sobre que quieres decidir')
execute_button = st.button('Ejecutar')

# Realizar la solicitud al API y mostrar los resultados si se ha presionado el botón de ejecución
if execute_button:
    response = make_decision(decision, analysis_type, 'concise')

    st.subheader('Results')

    if 'results' in response:
        for result in response['results']:
            if isinstance(result, dict):
                for analysis_type, analysis_result in result.items():
                    # Resto del código
                    st.markdown(f'# {analysis_type.upper()}')
                    if analysis_result is None:
                        st.write('No results available.')
                    elif isinstance(analysis_result, dict):
                        for key, value in analysis_result.items():
                            if isinstance(value, dict):
                                st.markdown(f'## {key.upper()}')
                                for sub_key, sub_value in value.items():
                                    st.markdown(f'### {sub_key}')
                                    st.write(sub_value)
                            else:
                                st.markdown(f'## {key.upper()}')
                                st.write(value)
                    elif isinstance(analysis_result, list):
                        for outcome in analysis_result:
                            if isinstance(outcome, dict):
                                st.markdown(f'## Outcome')
                                for key, value in outcome.items():
                                    st.markdown(f'### {key.upper()}')
                                    st.write(value)
                    else:
                        st.write('No results available.')
    else:
        st.write('No results available.')
