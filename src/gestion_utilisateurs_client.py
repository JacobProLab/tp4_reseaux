import socket
import glosocket


HEADER_NAME = "NAME"
HEADER_AGE = "AGE"

client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_soc.connect(("127.0.0.1", 1234))

print(glosocket.recv_mesg(client_soc))

message = " ".join([HEADER_NAME, input("Nom: ")])
glosocket.send_mesg(client_soc, message)

print(glosocket.recv_mesg(client_soc))

message = " ".join([HEADER_AGE, input("Age: ")])
glosocket.send_mesg(client_soc, message)

print(glosocket.recv_mesg(client_soc))

client_soc.close()


