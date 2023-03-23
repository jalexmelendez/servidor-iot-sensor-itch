import json
import uuid

import paho.mqtt.client as mqtt

from typing import Any, Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, BaseSettings

###########################################
# Configuracion de librerias y frameworks #
###########################################

class Settings(BaseSettings):
    # Configuracion MQTT
    MQTT_CHANNEL: str = "88e0f9a0/88e0f9a0-2248-41b5-bc8a-95f1484ce5ad"

    # Necesitamos un ID de cliente distinto en caso de tener diversas instancias del servidor.
    MQTT_CLIENT: str = f"TECNM_CHIH-{uuid.uuid4()}"
    MQTT_SERVER: str = "test.mosquitto.org"
    MQTT_PORT: int = 1883

# Instancia de FastAPI
app = FastAPI(
    title="API IOT SENSORES"
)
settings = Settings()

# Cliente de MQTT
client = mqtt.Client(settings.MQTT_CLIENT)

#################################
# Estructura de Datos y Modelos #
#################################

class DataLecture(BaseModel):
    """
    Esta es la estructura de datos de nuestra lectura por el sensor
    de arduino.
    """
    device_id: int
    frecuencia: Union[float, None]
    energia: Union[float, None]
    potencia: Union[float, None]
    fp: Union[float, None]
    corriente: Union[float, None]

#################
# Base de Datos #
#################

"""
Almacena datos en la lista en memoria, usado solo
en demostrar uso de mqtt, en azure se debe reemplazar
por mongo.
"""
MOCK_DATASTORE = []

def store_data(lecture: Any):
    """
    Esta es la funcion que nos ayuda a escribir en nuestra base de
    datos las lecturas recibidas por paho, convierte el json codificado en 
    una instancia de DataLecture.
    """
    casted_lecture: DataLecture = DataLecture(**lecture)
    print(f"Lectura recibida por MQTT: {casted_lecture}")
    # NOTA: Ejemplifica el proceso de almacenar datos, se debe de usar mongo para el proyecto.
    MOCK_DATASTORE.append(casted_lecture)

#####################
# Cliente MQTT Paho #
#####################

def on_connect(client, userdata, flags, rc):
    """
    La devolución de llamada para cuando el cliente recibe una respuesta CONNACK del servidor.
    """
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.MQTT_CHANNEL)

def on_disconnect(client, userdata,  rc):
    """
    El evento de desconexion.
    """
    print("El cliente se ha desconectado, iniciando proceso de intento de reconexion...")

def on_message(client, userdata, msg):
    """
    El callback cuando un PUBLISH message es recibido por el broker.
    """
    print(msg.topic+" "+str(msg.payload))
    try:
        bytes_to_json = json.loads(msg.payload)
        store_data(lecture=bytes_to_json)
    except Exception as e:
        print(e)

def on_publish(client, userdata, mid):
    """
    El Callback cuando un mensaje es publicado
    """
    print(f"Publicaste el mensaje: {mid}")

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.connect(host=settings.MQTT_SERVER, port=settings.MQTT_PORT, keepalive=60)

#
# Esto es parte de la interfaz de cliente con subprocesos. 
# Llame a esto una vez para iniciar un nuevo hilo para procesar el tráfico de red. 
# Esto proporciona una alternativa para llamar repetidamente a loop() usted mismo.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# loop_start() reconecta automaticamente, no es necesario hacer una reconexion manual.
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# NOTA: si se desea correr solamente PAHO sin fastapi comentar la linea "loop_start"
# y descomentar "loop_forever()"
 
# client.loop_forever()
client.loop_start()

####################
# Rutas de FastAPI #
# ##################

@app.get("/", tags=["Status"])
async def index():
    return {
        "status": 200
        }

@app.get("/mqtt-channel", tags=["MQTT"])
async def mqtt_channel():
    return {
        "channel": settings.MQTT_CHANNEL
        }

@app.get("/lectures", tags=["MQTT"])
async def lectures_index(page: int):
    return MOCK_DATASTORE

@app.post("/lectures", tags=["MQTT"])
async def create_lecture(lecture: DataLecture):
    lecture_to_json = jsonable_encoder(lecture)
    # Publicamos un mensaje via MQTT (PUB)
    client.publish(topic=settings.MQTT_CHANNEL, payload=json.dumps(lecture_to_json))
    return {
        "status": 200
        }
