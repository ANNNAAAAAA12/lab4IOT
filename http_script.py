import time
import json
import random
import urllib.request
import urllib.parse
import hmac
import hashlib
import base64
import asyncio
from azure.iot.device.aio import ProvisioningDeviceClient

SCOPE_ID = "0ne010B81EB"
DEVICE_ID = "dev-http-01"
DEVICE_KEY = "mTaWY7EgP12tYf3GCpIjsJsZbspM6065GjNxWgrNxzc="
PROVISIONING_HOST = "global.azure-devices-provisioning.net"

async def get_assigned_hub():
    client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=PROVISIONING_HOST,
        registration_id=DEVICE_ID,
        id_scope=SCOPE_ID,
        symmetric_key=DEVICE_KEY
    )
    res = await client.register()
    return res.registration_state.assigned_hub

def generate_sas_token(uri, key, expiry=3600):
    ttl = int(time.time()) + expiry
    sign_key = base64.b64decode(key)
    to_sign = f"{urllib.parse.quote_plus(uri)}\n{ttl}".encode('utf-8')
    raw_hmac = hmac.HMAC(sign_key, to_sign, hashlib.sha256).digest()
    signature = urllib.parse.quote_plus(base64.b64encode(raw_hmac))
    return f"SharedAccessSignature sr={urllib.parse.quote_plus(uri)}&sig={signature}&se={ttl}"

def send_http_telemetry(hub_hostname):
    resource_uri = f"{hub_hostname}/devices/{DEVICE_ID}"
    token = generate_sas_token(resource_uri, DEVICE_KEY)
    url = f"https://{hub_hostname}/devices/{DEVICE_ID}/messages/events?api-version=2021-04-12"

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    payload = {
        "temperatura": round(random.uniform(22.0, 25.0), 1),
        "humedad": round(random.uniform(50.0, 58.0), 1),
        "voltaje": round(random.uniform(3.2, 3.3), 2)
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            print(f"-> [HTTPS REST - {DEVICE_ID}] Status: {response.status} | Payload enviado: {payload}")
    except Exception as e:
        print(f"Error HTTPS: {e}")

if __name__ == "__main__":
    print(f"[DPS HTTP] Registrando dispositivo {DEVICE_ID}...")
    hub = asyncio.run(get_assigned_hub())
    print(f"--- [CAMINO TERCER PROTOCOLO: HTTP/HTTPS REST (Puerto 443)] ---")
    while True:
        send_http_telemetry(hub)
        time.sleep(10)
