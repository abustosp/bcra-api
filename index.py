from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

# Datos JSON proporcionados
response = requests.get("https://api.bcra.gob.ar/estadisticas/v3.0/Monetarias", verify=False)
json_data = response.text

# Función para filtrar los datos por fecha
def filtrar_por_fecha(data, desde, hasta):
    filtered_data = [entry for entry in data['results'] if desde <= entry['fecha'] <= hasta]
    return filtered_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener los datos del formulario
        endpoint_index = int(request.form['endpoint'])
        print(endpoint_index)
        fecha_desde = request.form['fecha_desde']
        fecha_hasta = request.form['fecha_hasta']
        print(fecha_hasta)
        
        # Cargar el JSON
        data = json.loads(json_data)
        id = str(data["results"][endpoint_index]["idVariable"])
        url = "https://api.bcra.gob.ar/estadisticas/v1/datosvariable/"+id+"/"+fecha_desde+"/"+fecha_hasta
        # Filtrar los datos por fecha
        #filtered_data = filtrar_por_fecha(data, fecha_desde, fecha_hasta)
        datos = requests.get(url, verify=False).json()
        endpoint = str(data["results"][endpoint_index]["descripcion"])
        
        return render_template('resultado.html', endpoint=endpoint, datos=datos)
    else:
        # Cargar el JSON
        data = json.loads(json_data)
        
        # Obtener los nombres de los endpoints disponibles
        endpoints = [entry['descripcion'] for entry in data['results']]
        
        return render_template('index.html', endpoints=endpoints)

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0')
