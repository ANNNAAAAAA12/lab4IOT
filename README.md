#Laboratorio 4: AMQP y HTTP/HTTPS REST en Azure IoT

Este repositorio contiene la implementación y evidencias para el envío de telemetría (temperatura, humedad e iluminación) hacia Azure IoT Central mediante los protocolos AMQP e HTTP/HTTPS REST.

#Dependencias e Instalación
Para ejecutar los scripts de este repositorio se requiere Python 3.8+ y las siguientes librerías:

pip install azure-iot-device requests

#Cómo Reproducir
1. Configuración previa (Sin Secretos)
Antes de ejecutar los scripts, asegúrate de reemplazar en el código o exportar tus credenciales de Azure IoT Central:

amqp_script.py: Cadena de conexión del dispositivo AMQP (dev-amqp-01).

http_script.py: Nombre de IoT Hub/Central, ID de dispositivo (dev-http-01) y clave primaria para la generación del token SAS HMAC-SHA256.

2. Ejecución de los scripts
   
# Transmisión por AMQP (Puerto 5671)
python3 amqp_script.py

# Transmisión por HTTP/HTTPS REST (Puerto 443)
python3 http_script.py
Estructura del Repositorio y Evidencias
amqp_script.py: Cliente de telemetría sobre protocolo AMQP.

http_script.py: Cliente de telemetría sobre protocolo HTTP/HTTPS REST con autenticación SAS.

/evidencias: Capturas de pantalla con las pruebas de ejecución, logs de transmisión y las 3 reglas de alerta configuradas en Azure IoT Central (Temperatura >26°C, Humedad >60% e Iluminación).
