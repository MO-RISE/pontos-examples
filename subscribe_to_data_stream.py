"Subscriber example for PONTOS datahub"
import logging
from paho.mqtt.client import Client

HOST = "pontos.ri.se"
PORT = 443
PATH = "/mqtt"
USERNAME = "__token__"
TOKEN = input("Please input your PONTOS HUB token: ")

SUBSCRIBE_PATTERN = "PONTOS_HUB/imo_8602713/#"

RETURN_CODES = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorized"
}

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s", level=logging.INFO
)

# Create client, explicitly specifying that the transport protocol should be websockets
client = Client(transport="websockets")
client.enable_logger(logging.getLogger("paho"))

# Specify the path where the broker listens for websocket connections
client.ws_set_options(path=PATH)

# Force transport protcol encryption through TLS (i.e. wss)
client.tls_set()

# Set username and password to be used for client auth upon connection
client.username_pw_set(USERNAME, TOKEN)

@client.connect_callback()
def on_connect(
    client, userdata, flags, reason_code
):
    logging.info(RETURN_CODES.get(reason_code)) if reason_code == 0 else logging.error(RETURN_CODES.get(reason_code))
    client.subscribe(SUBSCRIBE_PATTERN)

# Connect to client using the correct hostname and port
if client.connect(HOST, PORT) > 0:
    raise ConnectionRefusedError("Failed to connect to PONTOS!")


@client.message_callback()
def on_message(client, userdata, message):
    logging.info("Got message %s on topic %s", message.payload, message.topic)

# Blocking function that keep track of hearbeats, reconnections etc
client.loop_forever()