import json
import select
import socket
import sys

import glosocket
import protocol


def _make_socket() -> socket.socket:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(("127.0.0.1", 7777))
    soc.listen()
    return soc

def _make_ack(data: str) -> str:
    ack = json.dumps(protocol.Message(
        header=protocol.MyProtocol.OK,
        payload=data
    ))
    return ack

def _greet(soc: socket.socket):
    reply = _make_ack("Welcome to the server")
    glosocket.send_mesg(soc, reply)

def _tell(soc: socket.socket, payload: str):
    print(f"Client says: '{payload}'")
    reply = _make_ack("")
    glosocket.send_mesg(soc, reply)

def _bye(soc: socket.socket):
    reply = _make_ack("Your message was received, goodbye !")
    glosocket.send_mesg(soc, reply)

def _mainloop(server_soc: socket.socket):
    client_list: list[socket.socket] = []

    while True:
        result = select.select(client_list + [server_soc], [], [])
        readable_sockets: list[socket.socket] = result[0]

        for soc in readable_sockets:
            if soc == server_soc:
                new_soc, _ = server_soc.accept()
                client_list.append(new_soc)
            else:
                try:
                    data = glosocket.recv_mesg(soc)
                except glosocket.GLOSocketError:
                    client_list.remove(soc)
                    soc.close()
                    continue

                match json.loads(data):
                    case {"header": protocol.MyProtocol.GREET}:
                        _greet(soc)
                    case {"header": protocol.MyProtocol.TELL, "payload": payload}:
                        _tell(soc, payload)
                    case {"header": protocol.MyProtocol.QUIT}:
                        _bye(soc)
                        client_list.remove(soc)
                        soc.close()

def _main() -> int:
    try:
        soc = _make_socket()
    except OSError:
        print("Cannot create socket.")
        return 1
    try:
        _mainloop(soc)
    except KeyboardInterrupt:
        pass
    soc.close()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
