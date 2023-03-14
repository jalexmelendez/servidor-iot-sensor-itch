# Servidor IOT para sensor IOT ITCH

Este es el codigo fuente del servidor en python y cliente MQTT para almacenar las lectruas del sensor.

## TODO

- [ ] Conectar lecturas de datos de sensor
- [ ] Conectar base de datos MongoDB
- [ ] Desplegar a Azure

## Contenidos

1. Ejecutar app
2. Docs de app
3. Configuracion MQTT

### Ejecutar app

Primero debemos de crear nuestro entorno virtual

``` bash
# Buscar equivalente para OS, para linux es este comando

python3 -m venv env
```

Luego activar nuestro entorno

```bash
# buscar equivalente para OS

source env/bin/activate
```

Luego instalar las dependencias en requirements.txt

```bash
# buscar equivalente para OS

pip install -r requirements.txt
```

Ejecutar servidor

```bash
# buscar equivalente para OS
uvicorn main:app --reload

```

### Docs de app

Visita el link para ver la documentacion de la api

[http://localhost:8000/docs](http://localhost:8000/docs)

### Configuracion MQTT

La configuracion se encuentra en la parte superior del archivo, este es un ejemplo a usar
para trabajar con los publishers (sensores)

```python
# Confiuracion MQTT
MQTT_CHANNEL = "88e0f9a0/88e0f9a0-2248-41b5-bc8a-95f1484ce5ad"
MQTT_CLIENT = "{NOMBRE_SENSOR_IOT}"
```
