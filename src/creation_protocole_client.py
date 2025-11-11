import json
import socket
import sys

import glosocket
import protocol


def _make_socket() -> socket.socket:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("127.0.0.1", 7777))
    return soc

def _main() -> int:
    try:
        soc = _make_socket()
    except OSError:
        print("Cannot create socket")
        return 1
    
    # On cree un message
    greeting = protocol.Message(
        header=protocol.MyProtocol.GREET,
        payload=""
    )
    
    # On transforme le dictionnaire en une chaine de caractere JSON
    data = json.dumps(greeting)
    glosocket.send_mesg(soc, data)

    # On recupere la reponse sous forme de chaine de caractere puis
    # on charge un dictionnaire
    data = glosocket.recv_mesg(soc)
    reply = json.loads(data)

    # On verifie l'entete
    if reply["header"] != protocol.MyProtocol.OK:
        soc.close()
        return 1
    print(reply["payload"])

    message = input("Say something: ")
    tell = protocol.Message(
        header=protocol.MyProtocol.TELL,
        payload=message
    )
    glosocket.send_mesg(soc, json.dumps(tell))

    reply = json.loads(glosocket.recv_mesg(soc))
    if reply["header"] != protocol.MyProtocol.OK:
        soc.close()
        return 1
    
    bye = protocol.Message(
        header=protocol.MyProtocol.QUIT,
        payload=""
    )
    glosocket.send_mesg(soc, json.dumps(bye))

    reply = json.loads(glosocket.recv_mesg(soc))
    if reply["header"] != protocol.MyProtocol.OK:
        soc.close()
        return 1
    print(reply["payload"])
    
    soc.close()
    return 0


if __name__ =="__main__":
    sys.exit(_main())
