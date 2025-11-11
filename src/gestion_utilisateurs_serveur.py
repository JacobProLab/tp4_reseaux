import select
import socket
from typing import NoReturn

import glosocket


HEADER_NAME = "NOM"
HEADER_AGE = "AGE"
_client_list: list[socket.socket] = []


def _make_socket() -> socket.socket:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(("127.0.0.1", 1234))

def _remove_client_from_list(client: socket.socket) -> None:
    if client in _client_list:
        _client_list.remove(client)
    client.close()

def _try_send_message(destination: socket.socket, message: str) -> None:
    try:
        glosocket.send_mesg(destination, message)
    except glosocket.GLOSocketError:
        _remove_client_from_list(destination)

def _new_client(server_socket: socket.socket) -> None:
    client_socket, _ = server_socket.accept()

    # Une fois la connexion etablie, on ajoute le client a la liste
    _client_list.append(client_socket)
    _try_send_message(client_socket, "Bienvenue, quel est votre nom/age?")


def _get_name(data: str) -> str:
    return f"Bienvenue {data}"

def _get_age(data: str) -> str:
    return f"{data} ? Vous etes bien jeune !"

def _process_client(client_socket: socket.socket) -> None:
    try:
        message = glosocket.recv_mesg(client_socket)

        # Si le client s'est deconnecte, on le retire de la liste
    except glosocket.GLOSocketError:
        _remove_client_from_list(client_socket)
        return

    header, data = message.split(maxsplit=1)
    if header == HEADER_NAME:
        answer = _get_name(data)
    elif header == HEADER_AGE:
        answer = _get_age(data)
    
    _try_send_message(client_socket, answer)

def _main() -> NoReturn:
    server_socket = _make_socket()

    while True:

        # On passe a select comme premier argument une liste contenant les
        # sockets des clients et du serveur
        result = select.select(
            [server_socket] + _client_list,
            [],
            []
        )

        # Le resultat est un tuple de trois listes. La liste des sockets prets
        # a etre lu est toujours le premier element de ce tuple.
        readable_sockets: list[socket.socket] = result[0]

        for soc in readable_sockets:
            # Si le socket est celui du serveur, un nouveau client est en
            # en train de se connecter
            if soc == server_socket:
                _new_client(soc)
            # Sinon, on traite le client.
            else:
                _process_client(soc)


if __name__ == "__main__":
    _main()

