import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask import Flask

# Cargar los datos

df_tcsc_final = pd.read_csv(r"C:\Users\alvar\OneDrive\Escritorio\Trabajos AD\AD, Tecnofen\2 Datos\Tsecano_Cauquenes.csv")


# Inicializar Flask
server = Flask(__name__)

# Inicializar Dash y asociarlo al servidor Flask
app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Preparar las opciones para los Dropdowns
columnas_incluidas = df_tcsc_final.select_dtypes(include=['float64', 'object']).columns.tolist()
genotipos = df_tcsc_final['Genotipo'].unique().tolist()

# Diseñar el layout de la aplicación Dash
app.layout = html.Div([
    dcc.Dropdown(
        id='columna1-dropdown',
        options=[{'label': i, 'value': i} for i in columnas_incluidas],
        value=columnas_incluidas[0]
    ),
    dcc.Dropdown(
        id='columna2-dropdown',
        options=[{'label': i, 'value': i} for i in columnas_incluidas],
        value=columnas_incluidas[1]
    ),
    dcc.Dropdown(
        id='genotipo-dropdown',
        options=[{'label': i, 'value': i} for i in genotipos],
        value=genotipos[0]
    ),
    dcc.Graph(id='correlation-graph')
])

@app.callback(
    Output('correlation-graph', 'figure'),
    [Input('columna1-dropdown', 'value'),
     Input('columna2-dropdown', 'value'),
     Input('genotipo-dropdown', 'value')]
)
def update_graph(columna1, columna2, genotipo):
    df_filtrado = df_tcsc_final[df_tcsc_final['Genotipo'] == genotipo]
    
    # Convertir a numérico
    df_filtrado[columna1] = pd.to_numeric(df_filtrado[columna1], errors='coerce')
    df_filtrado[columna2] = pd.to_numeric(df_filtrado[columna2], errors='coerce')
    
    # Calcular correlaciones
    correlaciones = df_filtrado[[columna1, columna2]].corr().iloc[0, 1]
    
    # Crear gráfico
    fig = go.Figure(data=go.Scatter(x=df_filtrado[columna1], y=df_filtrado[columna2], mode='markers'))
    fig.update_layout(title=f"Correlación entre {columna1} y {columna2} para {genotipo}",
                      xaxis_title=columna1,
                      yaxis_title=columna2)
    return fig

# Ruta adicional de Flask
@server.route('/')
def index():
    return 'Bienvenido! Por favor visita /dashboard para ver el gráfico.'

if __name__ == '__main__':
    app.run_server(debug=True)
