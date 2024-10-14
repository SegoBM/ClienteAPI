from pydantic import BaseModel
from typing import List
import requests
from pydantic import parse_obj_as
from datetime import datetime  # Importa la librería datetime

# Modelo de datos para un terremoto
class Terremoto(BaseModel):
    id: str
    magnitude: float
    lugar: str
    fecha: str

# URL de la API con los parámetros ya incluidos
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Parámetros de la consulta
params = {
    "format": "geojson",
    "starttime": "2014-01-01",
    "endtime": "2014-01-02"
}

# Realiza la solicitud HTTP GET
response = requests.get(url, params=params)

# Verifica que la solicitud fue exitosa
if response.status_code == 200:
    # Obtiene los datos en formato JSON
    data = response.json()

    # Extrae las características de los terremotos
    terremotos_data = []
    for feature in data['features']:
        # Convierte el tiempo de milisegundos desde UNIX a un formato de fecha legible
        fecha_legible = datetime.utcfromtimestamp(feature['properties']['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        terremoto = Terremoto(
            id=feature['id'],
            magnitude=feature['properties']['mag'],
            lugar=feature['properties']['place'],
            fecha=fecha_legible  # Asigna la fecha legible
        )
        terremotos_data.append(terremoto)
    
    # Imprime los datos de los terremotos en consola
    for terremoto in terremotos_data:
        print(f"ID: {terremoto.id}, Magnitud: {terremoto.magnitude}, Lugar: {terremoto.lugar}, Fecha: {terremoto.fecha}")
else:
    print(f"Error en la solicitud: {response.status_code}")
