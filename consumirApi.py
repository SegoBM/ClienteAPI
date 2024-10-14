# Brian Segoviano Muñoz
# 20240621

from pydantic import BaseModel
import requests
from datetime import datetime 

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

# HTTP GET
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    terremotos_data = []
    for feature in data['features']:
        fecha_legible = datetime.utcfromtimestamp(feature['properties']['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        terremoto = Terremoto(
            id=feature['id'],
            magnitude=feature['properties']['mag'],
            lugar=feature['properties']['place'],
            fecha=fecha_legible  
        )
        terremotos_data.append(terremoto)
    
    # Imprime los datos de los terremotos en consola
    for terremoto in terremotos_data:
        print(f"ID: {terremoto.id}, Magnitud: {terremoto.magnitude}, Lugar: {terremoto.lugar}, Fecha: {terremoto.fecha}")
else:
    print(f"Error en la solicitud: {response.status_code}")