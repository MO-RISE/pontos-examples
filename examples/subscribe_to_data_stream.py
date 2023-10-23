"Subscriber example for PONTOS datahub"
import logging
from paho.mqtt.client import Client

HOST = "pontos.ri.se"
PORT = 443
PATH = "/mqtt"
USERNAME = "__token__"
TOKEN = input("Please input your PONTOS HUB token: ")

# This will listen in on all messages published by the vessel Burö (with IMO nr 8602713)
SUBSCRIBE_TOPIC = "PONTOS_EGRESS/imo_8602713/#"

RETURN_CODES = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorized",
}

# Some basic logging configuration to get nicely printed output
# The logging level is set to info here. You may want to use another level.
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s", level=logging.INFO
)

# Create client, explicitly specifying that the transport protocol should be websockets
client = Client(transport="websockets")

# Enabling the logger for the paho-mqtt library is a good thing. It makes it much easier
# to understand what may have happened in case of unexpected failures.
client.enable_logger(logging.getLogger("paho"))

# Specify the path where the broker listens for websocket connections
client.ws_set_options(path=PATH)

# Force transport protcol encryption through TLS (i.e. wss). This will use the default
# CA of the operating system to try to validate the authenticity of the broker. As such,
# there may be potential problems with older OS versions with outdated root certificates.
client.tls_set()

# Set username and password to be used for client auth upon connection
client.username_pw_set(USERNAME, TOKEN)


# Callback when client is connected to the broker. This is a good place
# to subscribe to whatever topics you would like to receive messages for.
@client.connect_callback()
def on_connect(client, userdata, flags, reason_code):
    if reason_code > 0:
        logging.error(RETURN_CODES.get(reason_code))
        return

    logging.info(RETURN_CODES.get(reason_code))
    client.subscribe(SUBSCRIBE_TOPIC)


# Connect to client using the correct hostname and port
if client.connect(HOST, PORT) > 0:
    raise ConnectionRefusedError("Failed to connect to PONTOS!")


# Callback when a new message is received on any of the subscribed topics
# In this example, we just log the output to the terminal.
@client.message_callback()
def on_message(client, userdata, message):
    logging.info("Got message %s on topic %s", message.payload, message.topic)


# Blocking function that keep track of hearbeats, reconnections etc
client.loop_forever()
