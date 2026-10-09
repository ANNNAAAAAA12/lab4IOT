import asyncio
import random
import time
from azure.iot.device.aio import ProvisioningDeviceClient, IoTHubDeviceClient

SCOPE_ID = "0ne010B81EB"
DEVICE_ID = "dev-amqp-01"
DEVICE_KEY = "LmCX/Qs4jWbdj78N8u+NmD27dFBJOw7cNBM6om67IJE="
PROVISIONING_HOST = "global.azure-devices-provisioning.net"

async def main():
    print(f"[DPS AMQP] Aprovisionando dispositivo {DEVICE_ID} vía AMQP...")
    prov_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=PROVISIONING_HOST,
        registration_id=DEVICE_ID,
        id_scope=SCOPE_ID,
        symmetric_key=DEVICE_KEY
    )
    result = await prov_client.register()
    
    if result.status != "assigned":
        print(f"Error en DPS: {result.status}")
        return

    assigned_hub = result.registration_state.assigned_hub
    print(f"-> ¡DPS Éxito! Hub asignado: {assigned_hub}")

    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=DEVICE_KEY,
        hostname=assigned_hub,
        device_id=DEVICE_ID
    )

    await device_client.connect()
    print("\n--- [CAMINO AMQP: PUERTO 5671] CONECTADO A AZURE IOT CENTRAL ---")

    try:
        while True:
            telemetria = {
                "temperatura": round(random.uniform(21.0, 27.0), 1),
                "humedad": round(random.uniform(48.0, 62.0), 1),
                "voltaje": round(random.uniform(3.1, 3.3), 2)
            }
            payload = str(telemetria).replace("'", '"')
            await device_client.send_message(payload)
            print(f"-> [AMQP - {DEVICE_ID}] Telemetría enviada: {payload}")
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        await device_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
