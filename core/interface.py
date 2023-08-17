import streamlit as st
import pandas as pd
import json





def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """

    return json.loads(response)
   
def generate_literal(sources):
    base_url = "https://storage.googleapis.com/xavinine"
    source_list = sources.strip().split('\n')
    
    links = []
    for source in source_list:
        _, filename = source.rsplit('/', 1)
        link = f' [<a href="{base_url}{source.replace("- .","")}">{filename}</a>] '
        links.append(link)
    
    links_literal = ', '.join(links)
    
    literal = f'Fuentes: {links_literal}'
    return literal

def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"],unsafe_allow_html=True)
        st.write(generate_literal(response_dict["sources"]),unsafe_allow_html=True)
      

    # Check if the response is a bar chart.
    if "bar-multiple" in response_dict:
        data = response_dict["bar-multiple"]["data"]
        columns = response_dict["bar-multiple"]["columns"]

        
        df = pd.DataFrame(data, columns=columns)
        df.set_index(columns[0], inplace=True)
        st.bar_chart(df)

    if "bar" in response_dict:
        data = response_dict["bar"]["data"]
        columns = response_dict["bar"]["columns"]

        
        df = pd.DataFrame(data, columns=columns)
        df.set_index(columns[0], inplace=True)
        st.bar_chart(df)
        

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]["data"]
        columns = response_dict["line"]["columns"]

        
        df = pd.DataFrame(data, columns=columns)
        df.set_index(columns[0], inplace=True)
        st.line_chart(df)

        # Check if the response is a line chart.
    if "line-multiple" in response_dict:
        data = response_dict["line-multiple"]["data"]
        columns = response_dict["line-multiple"]["columns"]

        
        df = pd.DataFrame(data, columns=columns)
        df.set_index(columns[0], inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)