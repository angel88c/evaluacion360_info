# Evaluación 360 iBtest - Visualizador de Comparativas

## Descripción
Esta aplicación web permite visualizar y comparar resultados de evaluaciones 360° mediante gráficos radar (spider charts). La herramienta facilita la comparación entre la autoevaluación y la evaluación recibida de otros, proporcionando una representación visual clara de las diferentes dimensiones evaluadas.

## Características
- Visualización de datos mediante gráficos radar
- Comparación entre evaluación 360° y autoevaluación
- Escala de evaluación del 1 al 10
- Interfaz intuitiva y fácil de usar
- Procesamiento de datos en formato texto

## Requisitos
- Python 3.x
- Dependencias listadas en `requirements.txt`

## Instalación
1. Clonar el repositorio
2. Crear un entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Unix/macOS
# o
.\env\Scripts\activate  # En Windows
```
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso
1. Ejecutar la aplicación:
```bash
streamlit run app.py
```
2. En la interfaz web:
   - Ingresar los datos de evaluación en el panel izquierdo
   - Ingresar los datos de autoevaluación en el panel derecho
   - Hacer clic en "Evaluar" para generar el gráfico comparativo

## Formato de Datos
Los datos deben ingresarse en el siguiente formato: