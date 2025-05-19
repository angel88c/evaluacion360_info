import re
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataclasses import dataclass

if "msg" not in st.session_state:
    st.session_state["msg"] = ''

@dataclass
class EvaluacionDimension:
    nombre: str
    resultado: float
    interpretacion: str

def get_data_from_text(text: str):
    
    try:
        # Expresión regular
        patron = r"^(.*?)\s+([\d.]+)\s+(.*)$"

        # Lista de objetos
        evaluaciones: list[EvaluacionDimension] = []

        # Parsear
        categorias = []
        for linea in text.strip().split('\n')[1:]:  # Saltar encabezado
            match = re.match(patron, linea)
            if match:
                nombre = match.group(1).strip()
                resultado = float(match.group(2))
                interpretacion = match.group(3).strip()
                evaluaciones.append(EvaluacionDimension(nombre, resultado, interpretacion))
                #print(f'{nombre}-{resultado}-{interpretacion}')
                
        return evaluaciones
    except Exception as e:
        st.error(e)


def create_dict_from_df_columns(df, col1, col2):
    """
    Creates a dictionary from two columns of a Pandas DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        col1 (str): The name of the column to use as keys.
        col2 (str): The name of the column to use as values.

    Returns:
        dict: A dictionary where keys are from col1 and values are from col2.
    """
    st.write(df.columns)
    st.write(col1, col2)
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError("One or both specified columns not found in DataFrame.")
    
    return dict(zip(df[col1], df[col2]))


if __name__ == "__main__":
    
    
    col1, col2 = st.columns(2)
    with col1:
        datos_e1 = st.text_area("Ingrese datos Evaluacion", height=400)
        
    with col2:
        datos_e2 = st.text_area("Ingrese datos Autoevaluacion", height=400)
    
    
    if st.button("Evaluar"):
        if not datos_e1 or not datos_e2:
            st.error("Debe llenar los datos de evaluacion y autoevaluacion")
            st.stop()
            
        evaluaciones_e1 = get_data_from_text(datos_e1)
        evaluaciones_e2 = get_data_from_text(datos_e2)
     
        if evaluaciones_e1 is None or evaluaciones_e2 is None:
            st.error("Formato incorrecto de textos")
            st.stop()
           
        categorias = [ev.nombre for ev in evaluaciones_e1]
       
        valores_1 = [ev.resultado for ev in evaluaciones_e1] + [evaluaciones_e1[0].resultado]
        valores_2 = [ev.resultado for ev in evaluaciones_e2] + [evaluaciones_e2[0].resultado]
        
        promedio_1 = np.mean(valores_1[:-1]) #Excluir el ultimo
        promedio_2 = np.mean(valores_2[:-1]) #Excluir el ultimo
        
        # Calcular ángulos
        angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
        angulos += [angulos[0]]
        
        # Streamlit
        st.title("Comparativa de Evaluación por Dimensión")
        st.markdown("Radar chart comparando dos resultados en escala del 1 al 10")

        # Crear figura
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Resultado 1
        ax.plot(angulos, valores_1, linewidth=1.5, linestyle='solid', label=f"Evaluacion 360 | {promedio_1}", color="blue")
        ax.fill(angulos, valores_1, alpha=0.2, color="darkblue")

        # Resultado 2
        ax.plot(angulos, valores_2, linewidth=1.5, linestyle='solid', label=f"Autoevaluacion 360 | {promedio_2}", color="teal")
        ax.fill(angulos, valores_2, alpha=0.2, color="teal")

        # Personalización
        #ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(1)
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=9)
        ax.set_yticks(range(1, 11))
        ax.set_yticklabels([str(i) for i in range(1, 11)])
        ax.set_ylim(0, 10)

        # Leyenda
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

        # Mostrar en Streamlit
        st.pyplot(fig)
        
        
    
    # file_loaded = st.file_uploader("Cargue el archivo de reporte de evaluacion")
    # if file_loaded is not None:
    #     # Can be used wherever a "file-like" object is accepted:
    #     dataframe = pd.read_csv(file_loaded, sep=",")
    #     st.write(dataframe)
    
    #     resultado_1_1 = create_dict_from_df_columns(dataframe, "Dimension", "Promedio")
    #     st.write(resultado_1_1)
    #     # Datos
    #     # Categorías
    #     resultado_1 = {
    #         "Calidad": 5,
    #         "Co-creación": 10,
    #         "Comunicación efectiva": 10,
    #         "Confía en tu intuición": 7,
    #         "Expertise Técnico": 8.5,
    #         "Liderazgo": 10,
    #         "Mejora continua": 10,
    #         "Relación con el cliente": 7,
    #         "Responsabilidad personal": 10,
    #         "Trabajo en equipo": 7
    #     }

    #     resultado_2 = {
    #         "Calidad": 7.4,
    #         "Co-creación": 7.8,
    #         "Comunicación efectiva": 8.5,
    #         "Confía en tu intuición": 8.2,
    #         "Expertise Técnico": 8.6,
    #         "Liderazgo": 7.8,
    #         "Mejora continua": 6.2,
    #         "Relación con el cliente": 8.8,
    #         "Responsabilidad personal": 8.2,
    #         "Trabajo en equipo": 7.6
    #     }

    #     categorias = list(resultado_1.keys())  # o define el orden tú mismo
    #     print(categorias)
    #     # Extraer los valores en el orden de categorías + cerrar figura
    #     valores_1 = [resultado_1[cat] for cat in categorias] + [resultado_1[categorias[0]]]
    #     valores_2 = [resultado_2[cat] for cat in categorias] + [resultado_2[categorias[0]]]
    #     print(valores_1)
    #     print(valores_2)
    #     # Calcular ángulos
    #     angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    #     angulos += [angulos[0]]
    #     
    #     # Streamlit
    #     st.title("Comparativa de Evaluación por Dimensión")
    #     st.markdown("Radar chart comparando dos resultados en escala del 1 al 10")

    #     # Crear figura
    #     fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    #     # Resultado 1
    #     ax.plot(angulos, valores_1, linewidth=2, linestyle='solid', label="Autoevaluacion")
    #     ax.fill(angulos, valores_1, alpha=0.2)

    #     # Resultado 2
    #     ax.plot(angulos, valores_2, linewidth=2, linestyle='solid', label="Evaluacion")
    #     ax.fill(angulos, valores_2, alpha=0.2)

    #     # Personalización
    #     #ax.set_theta_offset(np.pi / 2)
    #     ax.set_theta_direction(1)
    #     ax.set_xticks(angulos[:-1])
    #     ax.set_xticklabels(categorias, fontsize=9)
    #     ax.set_yticks(range(1, 11))
    #     ax.set_yticklabels([str(i) for i in range(1, 11)])
    #     ax.set_ylim(0, 10)

    #     # Leyenda
    #     ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    #     # Mostrar en Streamlit
    #     st.pyplot(fig)